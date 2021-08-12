import sys
import os
from hexhelper import HexHelper

class IPSPatcher:
    # Read the next hunk's data and apply it to the ROM file.
    @staticmethod
    def readAndApplyHunk(ipsFile, romFile):
        # Get the offset field
        offsetField = HexHelper.dataToHex(ipsFile.read(3))
        #print(offsetField)
        # If EOF, return False
        if offsetField == "454F46": # Spells out "EOF"
            print("Reached EOF successfully, finishing IPS patch...")
            return False
        # Get the length field
        lengthField = HexHelper.dataToHex(ipsFile.read(2))
        # Convert fields to integer
        patchOffset = HexHelper.hexToInt(offsetField)
        patchLength = HexHelper.hexToInt(lengthField)
        # Apply hunk.
        romFile.seek(patchOffset)
        if patchLength == 0:
            numRepeats = HexHelper.hexToInt(HexHelper.dataToHex(ipsFile.read(2)))
            byte = ipsFile.read(1)
            for i in range(numRepeats):
                romFile.write(byte)
        else:
            # Patches tend to be short - format enforced - so this shouldn't(?) raise any errors.
            bytes = ipsFile.read(patchLength)
            romFile.write(bytes)
        return True

    # Read the first 5 bytes to verify that this is an IPS file.
    @staticmethod
    def verifyFormat(ipsFile):
        verificationBytes = HexHelper.dataToHex(ipsFile.read(5))
        if verificationBytes == "5041544348": # Spells out "PATCH"
            return True
        else:
            return False

    # Apply an IPS patch to a ROM, given the paths of an IPS file and a ROM file.
    @staticmethod
    def applyIPSPatch(ipsPath, romPath):
        print(f"Applying patch from file {ipsPath}...")
        ipsFile = open(ipsPath, "rb")
        romFile = open(romPath, 'r+b', buffering = 0)
        if (IPSPatcher.verifyFormat(ipsFile)):
            while IPSPatcher.readAndApplyHunk(ipsFile, romFile):
                pass
            print(f"Finished applying patch {ipsPath} successfully.")
        else:
            print(f"CRITICAL ERROR: Provided IPS file {ipsPath} does not match the format specification!")
        ipsFile.close()
        romFile.close()

if __name__ == "__main__":
    print("Enter path to IPS file.")
    ipsPath = input()
    print("Enter path to ROM file.")
    romPath = input()
    IPSPatcher.applyIPSPatch(ipsPath, romPath)