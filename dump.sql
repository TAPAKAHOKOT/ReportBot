--
-- PostgreSQL database dump
--

-- Dumped from database version 11.12 (Raspbian 11.12-0+deb10u1)
-- Dumped by pg_dump version 11.12 (Raspbian 11.12-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.backup (
    customer_id integer NOT NULL,
    start_time timestamp without time zone
);


ALTER TABLE public.backup OWNER TO postgres;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    name_customer character varying(64),
    time_zone interval DEFAULT '03:00:00'::interval
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: start_working_time; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.start_working_time (
    user_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL
);


ALTER TABLE public.start_working_time OWNER TO postgres;

--
-- Name: start_wowrking_time; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.start_wowrking_time (
    user_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL
);


ALTER TABLE public.start_wowrking_time OWNER TO postgres;

--
-- Name: state_storage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state_storage (
    customer_id integer NOT NULL,
    name_tag character varying(128),
    name_status character varying(32)
);


ALTER TABLE public.state_storage OWNER TO postgres;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    tag_id integer NOT NULL,
    name_tag character varying(128),
    customer_id integer NOT NULL,
    update_time timestamp without time zone
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- Name: tag_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tag_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_tag_id_seq OWNER TO postgres;

--
-- Name: tag_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tag_tag_id_seq OWNED BY public.tag.tag_id;


--
-- Name: term; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.term (
    term_id integer NOT NULL,
    customer_id integer NOT NULL,
    name_tag character varying(128),
    name_status character varying(32),
    start_time timestamp without time zone,
    end_time timestamp without time zone
);


ALTER TABLE public.term OWNER TO postgres;

--
-- Name: term_term_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.term_term_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.term_term_id_seq OWNER TO postgres;

--
-- Name: term_term_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.term_term_id_seq OWNED BY public.term.term_id;


--
-- Name: users_tag_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_tag_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tag text NOT NULL,
    call_time timestamp without time zone NOT NULL
);


ALTER TABLE public.users_tag_history OWNER TO postgres;

--
-- Name: users_tag_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_tag_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_tag_history_id_seq OWNER TO postgres;

--
-- Name: users_tag_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_tag_history_id_seq OWNED BY public.users_tag_history.id;


--
-- Name: users_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_tags (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tag text NOT NULL,
    call_time timestamp without time zone NOT NULL
);


ALTER TABLE public.users_tags OWNER TO postgres;

--
-- Name: users_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_tags_id_seq OWNER TO postgres;

--
-- Name: users_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_tags_id_seq OWNED BY public.users_tags.id;


--
-- Name: users_work_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_work_statuses (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tag text NOT NULL,
    status text NOT NULL
);


ALTER TABLE public.users_work_statuses OWNER TO postgres;

--
-- Name: users_work_statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_work_statuses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_work_statuses_id_seq OWNER TO postgres;

--
-- Name: users_work_statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_work_statuses_id_seq OWNED BY public.users_work_statuses.id;


--
-- Name: works_times; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.works_times (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tag text NOT NULL,
    status text NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL
);


ALTER TABLE public.works_times OWNER TO postgres;

--
-- Name: works_times_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.works_times_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.works_times_id_seq OWNER TO postgres;

--
-- Name: works_times_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.works_times_id_seq OWNED BY public.works_times.id;


--
-- Name: tag tag_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag ALTER COLUMN tag_id SET DEFAULT nextval('public.tag_tag_id_seq'::regclass);


--
-- Name: term term_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.term ALTER COLUMN term_id SET DEFAULT nextval('public.term_term_id_seq'::regclass);


--
-- Name: users_tag_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_tag_history ALTER COLUMN id SET DEFAULT nextval('public.users_tag_history_id_seq'::regclass);


--
-- Name: users_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_tags ALTER COLUMN id SET DEFAULT nextval('public.users_tags_id_seq'::regclass);


--
-- Name: users_work_statuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_work_statuses ALTER COLUMN id SET DEFAULT nextval('public.users_work_statuses_id_seq'::regclass);


--
-- Name: works_times id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.works_times ALTER COLUMN id SET DEFAULT nextval('public.works_times_id_seq'::regclass);


--
-- Name: backup backup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backup
    ADD CONSTRAINT backup_pkey PRIMARY KEY (customer_id);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- Name: start_working_time start_working_time_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.start_working_time
    ADD CONSTRAINT start_working_time_pkey PRIMARY KEY (user_id);


--
-- Name: start_wowrking_time start_wowrking_time_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.start_wowrking_time
    ADD CONSTRAINT start_wowrking_time_pkey PRIMARY KEY (user_id);


--
-- Name: state_storage state_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.state_storage
    ADD CONSTRAINT state_storage_pkey PRIMARY KEY (customer_id);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (tag_id);


--
-- Name: term term_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.term
    ADD CONSTRAINT term_pkey PRIMARY KEY (term_id);


--
-- Name: users_tag_history users_tag_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_tag_history
    ADD CONSTRAINT users_tag_history_pkey PRIMARY KEY (id);


--
-- Name: users_tags users_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_tags
    ADD CONSTRAINT users_tags_pkey PRIMARY KEY (id);


--
-- Name: users_work_statuses users_work_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_work_statuses
    ADD CONSTRAINT users_work_statuses_pkey PRIMARY KEY (id);


--
-- Name: works_times works_times_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.works_times
    ADD CONSTRAINT works_times_pkey PRIMARY KEY (id);


--
-- Name: backup backup_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backup
    ADD CONSTRAINT backup_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(customer_id);


--
-- Name: tag tag_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(customer_id);


--
-- PostgreSQL database dump complete
--

