DROP TABLE IF EXISTS public.tblt2i;

CREATE TABLE IF NOT EXISTS public.tblt2i
(
    id serial primary key,
    positive text COLLATE pg_catalog."default",
    loras text COLLATE pg_catalog."default",
    negative text COLLATE pg_catalog."default",
    sampler character(50) COLLATE pg_catalog."default",
	steps character(50) COLLATE pg_catalog."default",
    cfg character(50) COLLATE pg_catalog."default",
    seed character(50) COLLATE pg_catalog."default",
    size character(50) COLLATE pg_catalog."default",
    modelhash character(50) COLLATE pg_catalog."default",
    model character(50) COLLATE pg_catalog."default",
    vaehash character(50) COLLATE pg_catalog."default",
    clipskip character(50) COLLATE pg_catalog."default",
    aDetailerModel character(50) COLLATE pg_catalog."default",
    aDetailerPrompt text COLLATE pg_catalog."default",
    aDetailerloras text COLLATE pg_catalog."default",
	faceRestoration character(50) COLLATE pg_catalog."default",
    block text COLLATE pg_catalog."default",
    bookmark int,
    filePath character(500) COLLATE pg_catalog."default",
    postedDate TIMESTAMPTZ DEFAULT Now(),
    createdDate TIMESTAMPTZ DEFAULT Now()
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblt2i
    OWNER to postgres;