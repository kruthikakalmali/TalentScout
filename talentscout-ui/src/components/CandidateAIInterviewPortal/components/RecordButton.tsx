import React from "react";
import { Icon, IconButton, useColorModeValue } from "@chakra-ui/react";
import { FaMicrophone, FaStop } from "react-icons/fa";

interface RecordButtonProps {
  onClick: () => void;
  isRecording: boolean;
  disabled?: boolean;
}

const RecordButton: React.FC<RecordButtonProps> = ({
  onClick,
  isRecording,
  disabled = false
}) => {
  const bg = useColorModeValue("red.500", "red.600");
  const hoverBg = useColorModeValue("red.600", "red.700");

  return (
    <IconButton
      aria-label={isRecording ? "Stop recording" : "Start recording"}
      icon={
        <Icon
          as={(isRecording ? FaStop : FaMicrophone) as any}
          boxSize="1.5em"
        />
      }
      isRound
      size="lg"
      h={16}
      w={16}
      fontSize="xl"
      bg={bg}
      color="white"
      _hover={{ bg: hoverBg }}
      onClick={onClick}
      disabled={disabled}
    />
  );
};

export default React.memo(RecordButton);
