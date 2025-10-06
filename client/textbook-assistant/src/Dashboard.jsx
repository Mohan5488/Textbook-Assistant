import { useEffect } from "react";

export default function Dashboard() {
  useEffect(() => {
    const fetchToken = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/get-token/", {
          credentials: "include", // Important: sends session cookie
        });
        if (!res.ok) throw new Error("Failed to fetch token");
        const data = await res.json();
        console.log("Token:", data.token);
        console.log("Login type:", data.login_type);

        localStorage.setItem("authToken", data.token);
      } catch (err) {
        console.error(err);
      }
    };

    fetchToken();
  }, []);

  return <h1>Dashboard</h1>;
}
