import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div style={{ textAlign: "center", padding: "4rem" }}>
      <h1>404 - Page Not Found</h1>
      <Link to="/">Return Home</Link>
    </div>
  );
};

export default NotFound;
