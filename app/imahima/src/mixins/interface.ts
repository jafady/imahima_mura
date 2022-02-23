export interface houseMate {
    id: string,
    name: string,
    icon: string,
    noticableStartTime: string,
    noticableEndTime: string,
    nowStatus: string,
    statusValidDateTime: Date,
}

export interface houseMates {[key:string]:houseMate}

export interface house {
    id:string,
    name:string,
}

export interface houseList {[key:string]:house}

export interface talk {
    message:string,
    userId:string,
    userName:string,
    date:string,
    time:string,
}

export interface event {
    id:string,
    eventName: string,
    recruitmentNumbersLower: number,
    recruitmentNumbersUpper: number|null,
    location: string,
    startDate: Date | null,
    startTime: string | null,
    endTime: string | null,
    displayDay: string,
    displayTime: string,
    categoryId: string,
    detail: string,
    userIds: string[]
}