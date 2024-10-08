import { Component } from "../core/component.js";

export class TypingGameWaiting extends Component {
  constructor(router, parameters, state) {
    super(router, parameters, state);
    this.connection = this.getRouteContext("WebSocket");
    this.findElement("button.go-back-to-game-home").onclick = this.onClick;
  }

  // onClick = (event) => {
  //     this.connection.close();
  // }

  get html() {
    return `
            <h1>waiting other paricipants...</h1>
            <h1>Don't reload this page.</h1>
            <button class="go-back-to-game-home">go back to game home</button>
        `;
  }
}
