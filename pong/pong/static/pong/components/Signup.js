import { Component } from "../core/component.js";

export class Signup extends Component {
	constructor(router, params, state) {
		super(router, params, state);
		this.findElement("form.signup-form").onsubmit = this.handleSignup;
	}

	handleSignup = async (event) => {
		event.preventDefault();
		const signupJson = JSON.stringify({
			"name": event.target.username.value,
			"password": event.target.password.value,
			"email": event.target.email.value,
		});
		try {
			await this.registerUser(signupJson);
			this.router.goNextPage("/");
		} catch (error) {
			alert(error);
		}
	}

	registerUser = async (jsonData) => {
		const response = await fetch("/pong/api/v1/auth/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: jsonData,
		});
		console.log(response);
		const data = await response.json();
		if (!response.ok) {
			throw Error(data.status);
		}
	}

	get html() {
		return `
			<div>
				<h1>Signup</h1>
				<form 
					action="/pong/oauth/42"
					method="GET"
					class="form-42oauth">
					<button class="form-42oauth" type=submit>42 Signup</button>
				</form>
				<form class="signup-form">
					<label for="username">Username</label>
					<input type=text placeholder="username" id="username" name="username" required></input><br/>
					<label for="password">Password</label>
					<input type=password placeholder="enter password" id="password" name="password" required></input><br/>
					<label for="repeat-password">Repeat Password</label>
					<input type=password placeholder="repeat password" id="repeat-password" name="repeat-password" required></input><br/>
					<label for="email">Email</label>
					<input type=email placeholder="email"id="email" name="email" required></input><br/>
					<button class="form-submit" type=submit>sign up</button>
				</form>
			</div>
		`;
	}
}
