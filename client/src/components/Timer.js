import React, { useState, useEffect } from 'react';

function Timer({bettingOver, betConfimation}) {
    const [seconds, setSeconds] = useState(20);

    useEffect(() => {
        if (seconds > 0) {
            const timerId = setTimeout(() => {
                setSeconds(seconds - 1)
            }, 1000)

            return () => clearTimeout(timerId);
        } else {
            console.log("TIMER DONE")
            bettingOver(true)
            betConfimation(true)
        }
    }, [seconds])

    return (
        <div>
            <h1>Timer: {seconds} seconds</h1>
        </div>
    )
}


export default Timer;