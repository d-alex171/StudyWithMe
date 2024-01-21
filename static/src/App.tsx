import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Basic from "./Basic";
import React from "react";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: "flex", gap: "12px" }}>
      </div>
      <Routes>
        <Route path="/" element={<Basic />} />
      </Routes>
    </BrowserRouter>
  );
}
