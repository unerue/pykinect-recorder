from ..k4arecord import _k4arecord


class Record:
    def __init__(self, device_handle, device_configuration, filepath):
        self.record_handle = _k4arecord.k4a_record_t()
        self.header_written = False
        self.create_recording(device_handle, device_configuration, filepath)
        
        self.add_imu_track()
        self.write_header()

    def __del__(self):
        self.flush()
        self.close()

    def create_recording(self, device_handle, device_configuration, filepath):
        _k4arecord.VERIFY(
            _k4arecord.k4a_record_create(
                filepath.encode("utf-8"),
                device_handle,
                device_configuration,
                self.record_handle,
            ),
            "Failed to create recording!",
        )

    def is_valid(self):
        return self.record_handle != None

    def close(self):
        if self.is_valid():
            _k4arecord.k4a_record_close(self.record_handle)
            self.record_handle = None

    def flush(self):
        if self.is_valid():
            _k4arecord.VERIFY(_k4arecord.k4a_record_flush(self.record_handle), "Failed to flush!")

    def write_header(self):
        if self.is_valid():
            _k4arecord.VERIFY(
                _k4arecord.k4a_record_write_header(self.record_handle),
                "Failed to write header!",
            )

    def write_imu(self, imu_sample):
        if self.is_valid():
            _k4arecord.VERIFY(
                _k4arecord.k4a_record_write_imu_sample(self.record_handle, imu_sample),
                "Failed to write imu!",
            )

    def write_capture(self, capture_handle):
        if not self.is_valid():
            raise NameError("Recording not found")
        _k4arecord.VERIFY(
            _k4arecord.k4a_record_write_capture(self.record_handle, capture_handle),
            "Failed to write capture!",
        )

    def add_imu_track(self):
        _k4arecord.VERIFY(
            _k4arecord.k4a_record_add_imu_track(self.record_handle),
            "Failed to add imu track!",
        )
