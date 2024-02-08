DROP TABLE IF EXISTS public.tbli2i;

CREATE TABLE IF NOT EXISTS public.tbli2i
(
    id serial primary key,
    positive character(250) COLLATE pg_catalog."default",
    negative character(250) COLLATE pg_catalog."default",
    sampler character(50) COLLATE pg_catalog."default",
	steps character(50) COLLATE pg_catalog."default",
    cfg character(50) COLLATE pg_catalog."default",
    seed character(50) COLLATE pg_catalog."default",
    size character(50) COLLATE pg_catalog."default",
    modelhash character(50) COLLATE pg_catalog."default",
    model character(50) COLLATE pg_catalog."default",
    vaehash character(50) COLLATE pg_catalog."default",
    denoisingStrength character(50) COLLATE pg_catalog."default", 
    clipskip character(50) COLLATE pg_catalog."default",
    aDetailerModel character(50) COLLATE pg_catalog."default",
    aDetailerPrompt character(250) COLLATE pg_catalog."default",
	faceRestoration character(50) COLLATE pg_catalog."default",
    block text COLLATE pg_catalog."default",
    bookmark int,
    postedDate TIMESTAMPTZ DEFAULT Now()
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tbli2i
    OWNER to postgres;