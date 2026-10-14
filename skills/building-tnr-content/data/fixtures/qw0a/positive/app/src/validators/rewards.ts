import { z } from "zod";
import { MasteryNames } from "@/drizzle/constants";

export const rewardFields = {
  reward_money: z.coerce.number().min(0).prefault(0),
  reward_flag: z.boolean().prefault(false),
  reward_mastery_stat: z.enum(["None", ...MasteryNames]).optional(),
};
