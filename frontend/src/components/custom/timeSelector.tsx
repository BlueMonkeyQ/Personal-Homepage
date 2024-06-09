import * as React from "react"

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

function generateTimes() {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
            const ampm = hour < 12 ? 'AM' : 'PM';
            const hour12 = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
            const displayTime = `${hour12.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')} ${ampm}`;
            const valueTime = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
            times.push({ displayTime, valueTime });
        }
    }
    return times;
}

const timeOptions = generateTimes();

export function TimeSelector({ setStartTime }: any) {
    const handleStartTimeChange = (selectedStartTime: string) => {
        setStartTime(selectedStartTime);
    };

    return (
        <Select onValueChange={handleStartTimeChange}>
            <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select a start time" />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel>Times</SelectLabel>
                    {timeOptions.map((time) => (
                        <SelectItem key={time.valueTime} value={time.valueTime}>
                            {time.displayTime}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    )
}