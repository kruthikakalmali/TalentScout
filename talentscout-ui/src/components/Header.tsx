// src/components/Header.tsx
import React from "react";
import { Box, Heading, useColorModeValue } from "@chakra-ui/react";

interface HeaderProps {
  title: string;
}

const Header: React.FC<HeaderProps> = ({ title }) => {
  // pick a single color that works in light/dark
  const bg = "linear(to-l, purple.700, blue.900)";

  return (
    <Box as="header" bgGradient={bg} boxShadow="md" px={6} py={4} textAlign="center">
      <Heading
        size="lg"
        letterSpacing="widest"
        color="white"
        fontFamily="'Poppins', sans-serif"  
      >
        {title}
      </Heading>
    </Box>
  );
};

export default React.memo(Header);
