import os

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from hamcrest import assert_that, equal_to, is_
from httpx import AsyncClient, codes

from filtration_app import models
from filtration_app.library.bandpass import BandPassFiltration
from filtration_app.library.containers import Range, Signal
from filtration_app.library.slta import SLTAFiltration, SLTAParameters
from filtration_app.routers import filtrations
from filtration_app_tests.helpers import build_url, create_sin_signal

load_dotenv()
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')


class TestFiltrationRouter:
    app = FastAPI()
    app.include_router(filtrations.router)
    frequency = 1000
    signal = create_sin_signal(
        duration=10,
        sin_frequencies=[1, 2, 3, 4],
        sin_amplitudes=[2, 3, 4, 5],
        signal_frequency=frequency
    )

    @pytest.mark.positive
    @pytest.mark.asyncio
    async def test_run_bandpass_filtration_positive(self):
        min_range, max_range = 2, 3

        bandpass = BandPassFiltration(
            signal=Signal(frequency=self.frequency, data=self.signal),
            frequency_range=Range(min_=min_range, max_=max_range)
        ).run()
        url = build_url(
            host=APP_HOST,
            port=APP_PORT,
            route_url='bandpass'
        )
        params = {
            'signal': models.Signal(
                frequency=self.frequency,
                data=self.signal.tolist()
            ).dict(),
            'frequency_range': models.Range(
                min_=min_range,
                max_=max_range
            ).dict()
        }
        async with AsyncClient(app=self.app) as client_ctx:
            response = await client_ctx.post(url=url, json=params)

        expected_value = models.Response(
            data=[
                models.Signal(
                    frequency=bandpass.frequency,
                    data=bandpass.data.tolist()
                )
            ]
        )
        assert_that(
            actual_or_assertion=response.raise_for_status(),
            matcher=is_(None)
        )
        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(codes.OK)
        )
        assert_that(
            actual_or_assertion=response.json(),
            matcher=equal_to(expected_value.dict(by_alias=True))
        )

    @pytest.mark.positive
    @pytest.mark.asyncio
    async def test_run_slta_filtration_positive(self):
        short_window, long_window, rank = 0.1, 1, 1
        slta_filtration_run = SLTAFiltration(
            signal=Signal(frequency=self.frequency, data=self.signal),
            parameters=SLTAParameters(
                short_window=short_window,
                long_window=long_window,
                rank=rank
            )
        ).run()
        url = build_url(
            host=APP_HOST,
            port=APP_PORT,
            route_url='slta'
        )
        params = {
            'signal': models.Signal(
                frequency=self.frequency,
                data=self.signal.tolist()
            ).dict(),
            'parameters': models.SLTAParameters(
                short_window=short_window,
                long_window=long_window,
                rank=rank
            ).dict()
        }
        async with AsyncClient(app=self.app) as client_ctx:
            response = await client_ctx.post(url=url, json=params)

        expected_value = models.Response(
            data=[
                models.Signal(
                    frequency=slta_filtration_run.frequency,
                    data=slta_filtration_run.data.tolist()
                )
            ]
        )
        assert_that(
            actual_or_assertion=response.raise_for_status(),
            matcher=is_(None)
        )
        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(codes.OK)
        )
        assert_that(
            actual_or_assertion=response.json(),
            matcher=equal_to(expected_value.dict(by_alias=True))
        )
