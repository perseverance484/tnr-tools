export const publicState = ["avatar", "level"] as const;
export const privateState = ["items"] as const;
export const allState = [...publicState, ...privateState] as const;
