import {
  Component,
  createContext,
  createEffect,
  createResource,
  createSignal,
} from "solid-js";
import { Body, redirect } from "solid-start";

interface SignInFormProps {
  setIsAuth: any;
  setIsToken: any;
}

type Response = {
  email: string;
  token: string;
  last_login: Date;
};

const SignInForm: Component<SignInFormProps> = (props) => {
  const [userInfo, setUserInfo] = createSignal({
    email: "",
    password: "",
  });

  async function handleLogin() {
    const loginFetch = await fetch("http://127.0.0.1:8000/auth/signin", {
      method: "post",
      body: JSON.stringify(userInfo()),
    })
      .then((res) => {
        return res.json();
      })
      .catch((err) => {
        return err;
      });

    const response = await loginFetch;
    const data: Response = response.data;

    if (data.token) {
      props.setIsToken(data.token);
      props.setIsAuth(true);
    }
  }

  return (
    <div>
      <form
        onsubmit={(e) => {
          e.preventDefault();
          handleLogin();
        }}
      >
        id :
        <input
          value={userInfo().email}
          onInput={(e) =>
            setUserInfo((prev) => ({ ...prev, email: e.currentTarget.value }))
          }
        ></input>
        <br />
        password :
        <input
          value={userInfo().password}
          onInput={(e) =>
            setUserInfo((prev) => ({
              ...prev,
              password: e.currentTarget.value,
            }))
          }
        ></input>
        <br />
        <button type="submit">로그인 하기</button>
      </form>
    </div>
  );
};

export default SignInForm;
