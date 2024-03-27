"""Module with API routes for filtration processes."""

from fastapi import APIRouter

from filtration_app.library.bandpass import BandPassFiltration
from filtration_app.library.slta import SLTAFiltration
from filtration_app.models import Range, Response, Signal, SLTAParameters

__all__ = [
    'router',
]

router = APIRouter()


@router.post('/bandpass')
async def run_bandpass_filtration(signal: Signal,
                                  frequency_range: Range) -> Response:
    """Return response with bandpass filtration result.

    Args:
        signal: pydantic Signal
        frequency_range: bandpass frequency interval [pydantic Range]

    Returns: Response

    """
    bandpass = BandPassFiltration(
        signal=Signal(
            frequency=signal.frequency,
            data=signal.convert_to_numpy_format()
        ),
        frequency_range=frequency_range
    ).run()

    return Response(
        data=[
            Signal(
                frequency=bandpass.frequency,
                data=bandpass.convert_to_list_format()
            )
        ]
    )


@router.post('/slta')
async def run_slta_filtration(signal: Signal,
                              parameters: SLTAParameters) -> Response:
    """Return response with SLTA filtration result.

    Args:
        signal: pydantic Signal
        parameters: pydantic SLTAParameters

    Returns: Response

    """
    filtration = SLTAFiltration(
        signal=Signal(
            frequency=signal.frequency,
            data=signal.convert_to_numpy_format()
        ),
        parameters=parameters
    ).run()

    return Response(
        data=[
            Signal(
                frequency=filtration.frequency,
                data=filtration.convert_to_list_format()
            )
        ]
    )