import {
  Component,
  createContext,
  createEffect,
  createResource,
  createSignal,
} from "solid-js";
import { Body } from "solid-start";

interface SignInFormProps {
  setIsAuth: boolean;
}

interface Data {
  email: string;
  password: string;
}

const SignInForm: Component<SignInFormProps> = (props) => {
  const [userInfo, setUserInfo] = createSignal({
    email: "",
    password: "",
  });

  const loginFetch = async () => {
    return await fetch("http://127.0.0.1:8000/auth/signin", {
      method: "post",
      body: JSON.stringify(userInfo()),
    }).then(console.log);
  };

  // createEffect(() => {});

  return (
    <div>
      <form
        onsubmit={(e) => {
          e.preventDefault();
          loginFetch();
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
