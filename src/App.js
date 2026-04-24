import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CareerForm from "./pages/CareerForm";
import Recommendations from "./pages/Recommendations";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CareerForm />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>
    </Router>
  );
}

export default App;