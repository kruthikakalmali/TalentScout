import React from "react";
import { HStack, Box, useColorModeValue } from "@chakra-ui/react";
import { keyframes } from "@emotion/react";

const bounce = keyframes`
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
`;

const Loader: React.FC = () => {
  const dotColor = useColorModeValue("purple.500", "purple.300");
  return (
    <HStack spacing="4px" justify="center">
      {[0, 0.2, 0.4].map((delay) => (
        <Box
          key={delay}
          w="20px"
          h="20px"
          bg={dotColor}
          borderRadius="50%"
          animation={`${bounce} 1.4s infinite ease-in-out both`}
          style={{ animationDelay: `${delay}s` }}
        />
      ))}
    </HStack>
  );
};

export default Loader;