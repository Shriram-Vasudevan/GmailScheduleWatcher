import * as React from "react"
import Image from "next/image";
import { useGmailServer } from "./hooks/useGmailServer";

export default function Home() {
  const { email, setEmail, subject, setSubject, message, setMessage, scheduledTime, setScheduledTime, scheduleEmail } = useGmailServer();
 
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1>Enter your email information</h1>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} />
      <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
      <input type="datetime-local" value={scheduledTime} onChange={(e) => setScheduledTime(e.target.value)} />
      <button onClick={scheduleEmail}>Schedule Email</button>
    </div>
  );
}
