import React, {Component, CSSProperties} from "react";
import { Link } from "react-router-dom";
import { Event } from "./models";
import ResourceManager from "./ResourceManager";

const user_email = (window as unknown as {User: string}).User;

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
            Currently logged in as {user_email}{' | '}
            <a href="/logout">Log out</a>
          </div>
        </div>
        <div className="row header">
          {this.renderMenuItem("/", this.props.event.name, {fontWeight: 800})}
          {this.state.events.length > 1 && this.renderMenuItem("/event-selector", "Switch events")}
          {this.renderMenuItem("/submit-playlist", "Submit songs")}
          {this.renderMenuItem("/rate", "Rate songs")}
          {this.renderMenuItem("/current_playlist", "Current Playlist")}
        </div>
      </>
    );
  }
}
