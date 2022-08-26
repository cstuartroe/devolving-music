import React, {Component, CSSProperties} from "react";
import { Link } from "react-router-dom";
import { Event } from "./models";
import { getAllowedPlatforms } from "./ChoosePlatform";
import ResourceManager from "./ResourceManager";

const w = (window as unknown as {User: string, IsAdmin: boolean});

type HeaderProps = {
  event: Event,
}

type HeaderState = {
  events: Event[],
}

export default class Header extends Component<HeaderProps, HeaderState>{
  constructor(props: HeaderProps) {
    super(props);

    this.state = {
      events: [],
    };
  }

  componentDidMount() {
    ResourceManager.getModels("events").then(events => this.setState({events}))
  }

  renderMenuItem(to: string, text: string, style?: CSSProperties) {
    return (
      <div className="menu-item" style={style}>
        <div>
          <Link to={to}>
            {text}
          </Link>
        </div>
      </div>
    );
  }

  render() {
    return (
      <>
        <div className="row email-bar">
          <div>
            Currently logged in as {w.User}{' | '}
            <a href="/logout">Log out</a>
            {w.IsAdmin && (
              <>
                {' | '}
                <a href="/admin/">Admin portal</a>
              </>
            )}
          </div>
        </div>
        <div className="row header">
          {this.renderMenuItem("/", this.props.event.name, {fontWeight: 800})}
          {this.state.events.length > 1 && this.renderMenuItem("/event-selector", "Switch events")}
          {getAllowedPlatforms(this.props.event).length > 0 && (
            this.renderMenuItem("/submit-playlist", "Submit songs")
          )}
          {this.renderMenuItem("/rate", "Rate songs")}
          {this.renderMenuItem("/current_playlist", "Current Playlist")}
          {this.renderMenuItem("/leaderboard", "Leaderboard")}
        </div>
      </>
    );
  }
}
