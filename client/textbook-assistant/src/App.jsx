import React from "react";

export default function App() {
  // Hardcode the full Google login URL
  const loginUrl = "http://127.0.0.1:8000/accounts/google/login/";

  return (
    <div className="login-box" style={styles.loginBox}>
      <h2>Sign in to your account</h2>
      <a href={loginUrl} className="login-button" style={styles.loginButton}>
        Continue with Google
      </a>
      
    </div>
  );
}

const styles = {
  loginBox: {
    background: "white",
    padding: "40px",
    borderRadius: "10px",
    display: "inline-block",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
    textAlign: "center",
    marginTop: "100px",
    fontFamily: "Arial, sans-serif",
  },
  loginButton: {
    backgroundColor: "#4285F4",
    color: "white",
    padding: "12px 24px",
    border: "none",
    borderRadius: "5px",
    fontSize: "16px",
    cursor: "pointer",
    textDecoration: "none",
  },
};
