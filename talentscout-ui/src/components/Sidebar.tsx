import React from "react";
import { Box, List, ListItem, Text, Image, useColorModeValue } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";

// Define the shape of each navigation item
interface NavItem {
  label: string;
  path: string;
}

// Configuration-driven list of sidebar links
const navItems: NavItem[] = [
  { label: "Recruiter Jobs Dashboard", path: "/recruiter" },
  { label: "Completed Interviews", path: "/recruiter/interview-completed-candidates" },
];

const Sidebar: React.FC = () => {
  const gradient = "linear(to-b, purple.700, blue.900)";
  const defaultTextColor = useColorModeValue("whiteAlpha.900", "whiteAlpha.900");
  const hoverAccent = useColorModeValue("purple.700", "purple.300");
  const itemBg = useColorModeValue("whiteAlpha.100", "whiteAlpha.200");
  const separatorColor = useColorModeValue("whiteAlpha.300", "whiteAlpha.400");

  return (
    <Box
      as="aside"
      w="250px"
      bgGradient={gradient}
      boxShadow="lg"
      display="flex"
      flexDirection="column"
      h="100vh"
    >
      {/* Logo at the top */}
      <Box mb={6} textAlign="center">
        <Image
          src="/talent_scout_logo.png"
          alt="Talent Scout Logo"
          mx="auto"
          h="200px"
        />
      </Box>

      {/* Dynamically render navigation links from config */}
      <List spacing={0} mt={4} flexGrow={1}>
        {navItems.map(({ label, path }, idx) => (
          <ListItem
            key={path}
            borderBottom={idx < navItems.length - 1 ? "1px solid" : undefined}
            borderBottomColor={separatorColor}
          >
            {/* Use 'end' prop for exact matching to avoid prefix matches */}
            <NavLink to={path} end style={{ textDecoration: 'none' }}>
              {({ isActive }) => (
                <Box
                  w="100%"
                  p={3}
                  bg={isActive ? 'whiteAlpha.800' : itemBg}
                  color={isActive ? hoverAccent : defaultTextColor}
                  _hover={{ bg: 'white', color: hoverAccent }}
                  transition="background 0.2s, color 0.2s"
                >
                  <Text fontSize="lg" fontWeight="medium" textAlign="center">
                    {label}
                  </Text>
                </Box>
              )}
            </NavLink>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default React.memo(Sidebar);
