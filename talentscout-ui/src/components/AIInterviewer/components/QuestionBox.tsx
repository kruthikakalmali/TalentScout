import React from 'react';
import { Box, Text } from '@chakra-ui/react';

interface QuestionBoxProps {
  question: string;
}

const QuestionBox: React.FC<QuestionBoxProps> = ({ question }) => (
  <Box
    mb={6}
    p={6}
    bg="whiteAlpha.100"
    border="1px solid"
    borderColor="whiteAlpha.200"
    borderRadius="md"
    boxShadow="sm"
    w="100%"
  >
    <Text fontSize="xl" fontWeight="semibold" color="whiteAlpha.900">
      {question}
    </Text>
  </Box>
);

export default React.memo(QuestionBox);