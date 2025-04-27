import React from "react";
import { Box, Heading } from "@chakra-ui/react";

interface Header {
  title: string;
}

const Header: React.FC<Header> = ({ title }) => (
  <Box
    bgGradient="linear(to-r, purple.700, blue.900)"
    boxShadow="lg"
    px={6}
    py={4}
  >
    <Heading size="lg" letterSpacing="widest" color="whiteAlpha.900">
      {title}
    </Heading>
  </Box>
);

export default React.memo(Header);
