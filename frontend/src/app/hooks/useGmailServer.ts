import * as React from "react"

export const useGmailServer = () => {
    const serverURL = process.env.NEXT_PUBLIC_SERVER_URL;

    const [email, setEmail] = React.useState("");
    const [subject, setSubject] = React.useState("");
    const [message, setMessage] = React.useState("");
    const [scheduledTime, setScheduledTime] = React.useState("");

    const scheduleEmail = async () => {
        return await fetch(`${serverURL}/schedule-email`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, subject, message, scheduledTime }),
        });
    }

    return {
        email, setEmail,
        subject, setSubject,
        message, setMessage,
        scheduledTime, setScheduledTime,
        scheduleEmail,
    }
}