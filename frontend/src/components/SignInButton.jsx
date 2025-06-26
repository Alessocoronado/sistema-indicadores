import React from 'react';
import { useMsal } from '@azure/msal-react';
import { authApi } from '@/lib/api';

const SignInButton = () => {
  const { instance, accounts } = useMsal();

  const handleLogin = async () => {
    try {
      const response = await instance.loginPopup();
      const token = response.accessToken;
      if (token) {
        await authApi.verifyToken(token);
      }
    } catch (err) {
      console.error('Login error', err);
    }
  };

  const handleLogout = () => {
    instance.logoutPopup();
  };

  if (accounts.length > 0) {
    return (
      <button onClick={handleLogout} className="px-3 py-2 bg-white text-black rounded-md">Salir</button>
    );
  }

  return (
    <button onClick={handleLogin} className="px-3 py-2 bg-white text-black rounded-md">Iniciar sesión</button>
  );
};

export default SignInButton;
