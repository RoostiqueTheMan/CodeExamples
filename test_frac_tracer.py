class TestFracTracer:

    @pytest.mark.positive
    @patch.object(FracTracer, 'azimuth', new_callable=PropertyMock)
    @patch.object(FracTracer, 'get_median_azimuth')
    def test_correct_attributes_positive(self, mock_get_median_azimuth: Mock,
                                         mock_azimuth: Mock):
        median_azimuth = 'median_azimuth'
        mock_get_median_azimuth.return_value = median_azimuth
        events_cloud = np.array([[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]])
        port_point = Coordinate(x=0, y=10, altitude=-1000)
        radius_start_area = 10
        well = VectorDirection(azimuth=3 * PI / 2, inclination=0.5)
        azimuth = PI
        mock_azimuth.return_value = azimuth

        frac_tracer = create_frac_tracer_instance(
            events_cloud=events_cloud,
            port_point=port_point,
            radius_start_area=radius_start_area,
            well=well
        )
        assert_that(
            actual_or_assertion=np.array_equal(
                frac_tracer._FracTracer__events_cloud, events_cloud
            ),
            matcher=is_(True)
        )
        assert_that(
            actual_or_assertion=frac_tracer._FracTracer__port_point,
            matcher=equal_to(port_point)
        )
        assert_that(
            actual_or_assertion=frac_tracer._FracTracer__radius_start_area,
            matcher=equal_to(radius_start_area)
        )
        assert_that(
            actual_or_assertion=frac_tracer._FracTracer__median_azimuth,
            matcher=equal_to(median_azimuth)
        )
        assert_that(
            actual_or_assertion=frac_tracer._FracTracer__well,
            matcher=equal_to(well)
        )

    @pytest.mark.positive
    @pytest.mark.parametrize(
        ['events_cloud', 'expected_value'],
        [
            (np.array([[0, 1, 2, 3, 4], [4, 7, 5, 3, 4], [0, 11, 5, 2, 0]]),
             [0, 1, 2]),
            (np.array([[0, 1, 90, 99, 4], [1, 7, 89, 9, 4], [0, 1, 2, 99, 4]]),
             []),
            (np.array([[0, 1, 2, 3, 4], [1, 15, 101, 9, 4], [0, 2, 2, 5, 4]]),
             [0, 2]),

        ]
    )
    def test_get_events_in_start_area_positive(self, events_cloud: np.array,
                                               expected_value: List[int]):
        frac_tracer = create_frac_tracer_instance(
            events_cloud=events_cloud,
            radius_start_area=20,
            port_point=Coordinate(
                x=0, y=10, altitude=-10
            )
        )
        assert_that(
            actual_or_assertion=list(frac_tracer.get_events_in_start_area()),
            matcher=equal_to(expected_value)
        )

    @pytest.mark.negative
    @patch.object(Vector, '__init__')
    def test_get_events_in_start_area_negative(self, mock_vector: Mock):
        mock_vector.side_effect = ValueError
        actual_value = create_frac_tracer_instance().get_events_in_start_area()

        assert_that(
            actual_or_assertion=list(actual_value),
            matcher=equal_to([])
        )

    @pytest.mark.positive
    def test_get_median_azimuth_positive(self):
        frac_tracer = create_frac_tracer_instance(
            events_cloud=np.array(
                [[0, 1, 2, 3, 4], [4, 7, 5, 3, 4], [0, 11, 5, 2, 0]]
            ),
            port_point=Coordinate(
                x=0, y=10, altitude=-10
            )
        )
        radians_diff = abs(frac_tracer.get_median_azimuth() - 2.583)

        assert_that(
            actual_or_assertion=radians_diff < RADIANS_ACCURACY,
            matcher=is_(True)
        )