import { Switch, Match, Component, createEffect, createSignal } from "solid-js";
import { Router, Routes, Route } from "@solidjs/router";
import SignInForm from "./forms/signin";
import Main from "./pages/main";
import SignUpForm from "./forms/signup";
import { redirect } from "solid-start";

export type User = {
  id: string;
  password: string;
};

const App: Component = () => {
  const [isAuth, setIsAuth] = createSignal(false);
  const [isToken, setIsToken] = createSignal("");

  createEffect(() => {
    isAuth();
  });

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Main isAuth={isAuth} />} />
          <Route
            path="/signin"
            element={
              <SignInForm setIsAuth={setIsAuth} setIsToken={setIsToken} />
            }
          />
          <Route path="/signup" element={<SignUpForm />} />
        </Routes>
      </Router>
      <br />
      {/* <button onclick={() => render(() => S)}>회원가입 하기</button> */}
    </div>
  );
};

export default App;
