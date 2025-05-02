import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const authenticated = useSelector(state => state.auth.authenticated);
  return authenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;