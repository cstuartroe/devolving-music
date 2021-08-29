import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "../static/scss/main.scss";

class App extends Component {
  createEvent = () => {
    fetch("/api/submit_spotify_playlist", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        event: 1,
        playlist_link: "https://open.spotify.com/playlist/53S1fz2n5dUfhkXyEC5JuS?si=d433af83b1d841c1",
      })
    })
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact={true} path="/" render={() => (
            <div>
              <p>Hello, World!</p>
              <a onClick={this.createEvent}>Create event</a>
            </div>
          )}/>
        </Switch>
      </Router>
    );
  }
}

export default App;
