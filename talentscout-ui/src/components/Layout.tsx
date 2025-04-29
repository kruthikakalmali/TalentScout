import React from "react"
import { Flex, Box } from "@chakra-ui/react"
import Header from "./Header"
import Sidebar from "./Sidebar"

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => (
    <Flex flex="1" overflow="hidden">
      <Sidebar />
      <Box flex="1" overflowY="auto">
        {children}
      </Box>
    </Flex>
)

export default Layout