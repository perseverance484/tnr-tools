import { z } from "zod";

export const makeCappedNullableNumber = (max: number) =>
  z.preprocess(
    (value) => (value === "" || value === null || value === undefined ? null : value),
    z.coerce.number().int().min(0).max(max).nullable(),
  );

export const strictNullOnly = (max: number) =>
  z.preprocess(
    (value) => (value === null ? null : value),
    z.coerce.number().int().min(0).max(max).nullable(),
  );
