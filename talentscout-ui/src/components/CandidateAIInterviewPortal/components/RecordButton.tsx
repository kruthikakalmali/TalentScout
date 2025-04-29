import React from "react";
import { IconButton, Icon, useColorModeValue } from "@chakra-ui/react";
import { keyframes } from "@emotion/react";
import { FaMicrophone, FaStop } from "react-icons/fa";

interface RecordButtonProps {
  onClick: () => void;
  isRecording: boolean;
  disabled?: boolean;
}

// pulse animation using emotion keyframes
const pulseRing = keyframes`
  0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
  70% { box-shadow: 0 0 0 12px rgba(255, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
`;

export const RecordButton: React.FC<RecordButtonProps> = ({ onClick, isRecording, disabled = false }) => {
  const bg = useColorModeValue("red.400", "red.500");
  const hoverBg = useColorModeValue("red.500", "red.600");
  const iconColor = useColorModeValue("white", "white");

  return (
    <IconButton
      aria-label={isRecording ? "Stop recording" : "Start recording"}
      icon={<Icon as={(isRecording ? FaStop : FaMicrophone) as any} boxSize="1.5em" />}
      isRound
      size="lg"
      h={16}
      w={16}
      fontSize="2xl"
      bg={bg}
      color={iconColor}
      border="2px solid"
      borderColor="whiteAlpha.400"
      boxShadow="lg"
      _hover={{ bg: hoverBg, transform: "scale(1.1)" }}
      _active={{ transform: "scale(0.95)" }}
      transition="all 0.2s ease"
      onClick={onClick}
      disabled={disabled}
      sx={isRecording ? { animation: `${pulseRing} 1.5s infinite` } : {}}
    />
  );
};

export default React.memo(RecordButton);