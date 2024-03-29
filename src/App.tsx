import React, { Component } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";


import "../static/scss/main.scss";
import ResourceManager from "./ResourceManager";
import { Event, Artist_platform } from "./models";
import Header from "./Header";
import Home from "./Home";
import EventSelector from "./EventSelector";
import ChoosePlatform from "./ChoosePlatform";
import SubmitPlaylist from "./SubmitPlaylist";
import RateSongs from "./RateSongs";
import DuplicatesReviewer from "./DuplicatesReviewer";
import CurrentPlaylist from "./CurrentPlaylist";
import LeaderboardPage from "./Leaderboard";


const event_key = "selected_event";

type AppState = {
  event?: Event,
}

class App extends Component<{}, AppState> {
  constructor(props: {}) {
    super(props);

    this.state = {};
  }

  getSelectedEvent() {
    const event_id_string = localStorage.getItem(event_key);
    const event_id = event_id_string ? parseInt(event_id_string) : null;

    ResourceManager.getModels("events").then(events => {
      const found = events.find(event => event.id === event_id);

      const event = found ? found : events[0];

      this.setEvent(event);
    })
  }

  setEvent(event: Event) {
    localStorage.setItem(event_key, event.id.toString());
    this.setState({event});
  }

  componentDidMount() {
    this.getSelectedEvent();
  }

  render() {
    const { event } = this.state;

    if (event === undefined) {
      return null;
    } else {
      return (
        <Router>
          <div id="main-container" className="container-fluid">
            <Header event={event}/>

            <div className="row">
              <div className="col-12 col-md-2"/>
              <div className="col-12 col-md-8">
                <Routes>
                  <Route path="/">
                    <Route index element={<Home event={event}/>}/>

                    <Route path="event-selector"
                           element={<EventSelector setEvent={this.setEvent.bind(this)}/>}
                    />

                    <Route path="submit-playlist">
                      <Route index element={<ChoosePlatform event={event}/>}/>
                      {Artist_platform.map(platform => (
                        <Route path={platform} key={platform} element={
                          <SubmitPlaylist platform={platform} event={event}/>
                        }/>
                      ))}
                    </Route>

                    <Route path="rate" element={<RateSongs event={event}/>}/>

                    <Route path="duplicates" element={<DuplicatesReviewer event={event}/>}/>

                    <Route path="current_playlist" element={<CurrentPlaylist event={event}/>}/>

                    <Route path="leaderboard" element={<LeaderboardPage event={event}/>}/>

                    <Route path="*" element={<Navigate replace to="/"/>}/>
                  </Route>
                </Routes>
              </div>
            </div>
          </div>
        </Router>
      );
    }
  }
}

export default App;
