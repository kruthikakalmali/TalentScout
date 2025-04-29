import React from "react";
import { Box, Text } from "@chakra-ui/react";

interface SmallRecordingsListProps {
  recordings: string[];
}

export const SmallRecordingsList: React.FC<SmallRecordingsListProps> = ({ recordings }) => {
  if (!recordings.length) return <Text color="whiteAlpha.700">No recordings yet.</Text>;
  return (
    <Box>
      {recordings.map((src, idx) => (
        <Box key={idx} mb={2}>
          <Text fontSize="sm" color="whiteAlpha.800" mb={1}>Clip #{idx + 1}</Text>
          <audio controls src={src} style={{ width: '100%' }} />
        </Box>
      ))}
    </Box>
  );
};
