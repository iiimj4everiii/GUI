class Color:

    @staticmethod
    def rgb_to_hex(rgb: tuple):
        def pad_hex(hex_str: str):
            if len(hex_str) == 1:
                return '0' + hex_str
            return hex_str

        assert len(rgb) == 3

        hex_str = '#'
        for intensity in rgb:
            intensity_hex = hex(int(intensity))[2:]
            hex_str += pad_hex(intensity_hex)

        return hex_str
