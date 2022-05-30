import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import ResourceManager from "./ResourceManager";
import { Event } from "./models";


export type event_setter = (e: Event) => void;

type EventSelectorProps = {
  setEvent: event_setter,
}

type EventSelectorState = {
  events?: Event[],
  submitted: boolean,
}

export default class EventSelector extends Component<EventSelectorProps, EventSelectorState>{
  constructor(props: EventSelectorProps) {
    super(props);

    this.state = {
      submitted: false,
    }
  }

  componentDidMount() {
    ResourceManager.getModels("events").then(events => this.setState({events}));
  }

  render() {
    if (this.state.submitted) {
      return <Redirect to="/"/>
    }

    if (this.state.events === undefined) {
      return null;
    } else {
      return (
        <div className="row">
          <div className="col-12">
            <h2>Select an event:</h2>
          </div>
          {this.state.events.sort((e1, e2) => e1.date.localeCompare(e2.date))
            .map(event => (
            <div key={event.id}
                 className="col-12 event-card">
              <div className="event-card-image"
                   style={{
                     backgroundImage: `url("${event.image}")`,
                   }}
                   onClick={() => {
                     this.props.setEvent(event);
                     this.setState({submitted: true});
                   }}
              >
                <div className="event-card-inner">
                  {event.name}
                </div>
              </div>
            </div>
          ))}
        </div>
      );
    }
  }
}
