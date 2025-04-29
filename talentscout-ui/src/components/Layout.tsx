import React from "react";
import { Flex, Box } from "@chakra-ui/react";
import Sidebar from "./Sidebar";
import ChatWidget from "./HRJobPortal/ChatWidget";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => (
    <Flex flex="1" overflow="hidden">
      <Sidebar />
      <Box flex="1" overflowY="auto">
        {children}
      </Box>
      <ChatWidget />
    </Flex>
);

export default Layout;