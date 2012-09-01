--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articles_article; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_article (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    slug character varying(50) NOT NULL,
    status_id integer NOT NULL,
    author_id integer NOT NULL,
    keywords text NOT NULL,
    description text NOT NULL,
    markup character varying(1) DEFAULT 'h'::character varying NOT NULL,
    content text NOT NULL,
    rendered_content text NOT NULL,
    publish_date timestamp with time zone DEFAULT '2012-08-17 19:37:07.697004-04'::timestamp with time zone NOT NULL,
    expiration_date timestamp with time zone,
    is_active boolean DEFAULT true NOT NULL,
    login_required boolean DEFAULT false NOT NULL,
    use_addthis_button boolean DEFAULT true NOT NULL,
    addthis_use_author boolean DEFAULT true NOT NULL,
    addthis_username character varying(50) NOT NULL,
    auto_tag boolean NOT NULL
);


ALTER TABLE public.articles_article OWNER TO postgres;

--
-- Name: articles_article_followup_for; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_article_followup_for (
    id integer NOT NULL,
    from_article_id integer NOT NULL,
    to_article_id integer NOT NULL
);


ALTER TABLE public.articles_article_followup_for OWNER TO postgres;

--
-- Name: articles_article_followup_for_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_followup_for_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_article_followup_for_id_seq OWNER TO postgres;

--
-- Name: articles_article_followup_for_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_followup_for_id_seq OWNED BY articles_article_followup_for.id;


--
-- Name: articles_article_followup_for_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_followup_for_id_seq', 1, false);


--
-- Name: articles_article_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_article_id_seq OWNER TO postgres;

--
-- Name: articles_article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_id_seq OWNED BY articles_article.id;


--
-- Name: articles_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_id_seq', 1, false);


--
-- Name: articles_article_related_articles; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_article_related_articles (
    id integer NOT NULL,
    from_article_id integer NOT NULL,
    to_article_id integer NOT NULL
);


ALTER TABLE public.articles_article_related_articles OWNER TO postgres;

--
-- Name: articles_article_related_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_related_articles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_article_related_articles_id_seq OWNER TO postgres;

--
-- Name: articles_article_related_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_related_articles_id_seq OWNED BY articles_article_related_articles.id;


--
-- Name: articles_article_related_articles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_related_articles_id_seq', 1, false);


--
-- Name: articles_article_sites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_article_sites (
    id integer NOT NULL,
    article_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE public.articles_article_sites OWNER TO postgres;

--
-- Name: articles_article_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_article_sites_id_seq OWNER TO postgres;

--
-- Name: articles_article_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_sites_id_seq OWNED BY articles_article_sites.id;


--
-- Name: articles_article_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_sites_id_seq', 1, false);


--
-- Name: articles_article_tags; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_article_tags (
    id integer NOT NULL,
    article_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.articles_article_tags OWNER TO postgres;

--
-- Name: articles_article_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_article_tags_id_seq OWNER TO postgres;

--
-- Name: articles_article_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_tags_id_seq OWNED BY articles_article_tags.id;


--
-- Name: articles_article_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_tags_id_seq', 1, false);


--
-- Name: articles_articlestatus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_articlestatus (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    ordering integer DEFAULT 0 NOT NULL,
    is_live boolean DEFAULT false NOT NULL
);


ALTER TABLE public.articles_articlestatus OWNER TO postgres;

--
-- Name: articles_articlestatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_articlestatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_articlestatus_id_seq OWNER TO postgres;

--
-- Name: articles_articlestatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_articlestatus_id_seq OWNED BY articles_articlestatus.id;


--
-- Name: articles_articlestatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_articlestatus_id_seq', 2, true);


--
-- Name: articles_attachment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_attachment (
    id integer NOT NULL,
    article_id integer NOT NULL,
    attachment character varying(100) NOT NULL,
    caption character varying(255) NOT NULL
);


ALTER TABLE public.articles_attachment OWNER TO postgres;

--
-- Name: articles_attachment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_attachment_id_seq OWNER TO postgres;

--
-- Name: articles_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_attachment_id_seq OWNED BY articles_attachment.id;


--
-- Name: articles_attachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_attachment_id_seq', 1, false);


--
-- Name: articles_tag; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE articles_tag (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    slug character varying(64)
);


ALTER TABLE public.articles_tag OWNER TO postgres;

--
-- Name: articles_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.articles_tag_id_seq OWNER TO postgres;

--
-- Name: articles_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_tag_id_seq OWNED BY articles_tag.id;


--
-- Name: articles_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_tag_id_seq', 1, false);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 129, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: content_copy; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_copy (
    id integer NOT NULL,
    page_id integer,
    name character varying(256),
    context character varying(32) NOT NULL,
    text character varying(1024) DEFAULT 'change me'::character varying NOT NULL
);


ALTER TABLE public.content_copy OWNER TO postgres;

--
-- Name: content_copy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_copy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_copy_id_seq OWNER TO postgres;

--
-- Name: content_copy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_copy_id_seq OWNED BY content_copy.id;


--
-- Name: content_copy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_copy_id_seq', 1, false);


--
-- Name: content_designimage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_designimage (
    id integer NOT NULL,
    page_id integer,
    name character varying(256),
    context character varying(32) NOT NULL,
    src character varying(300)
);


ALTER TABLE public.content_designimage OWNER TO postgres;

--
-- Name: content_designimage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_designimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_designimage_id_seq OWNER TO postgres;

--
-- Name: content_designimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_designimage_id_seq OWNED BY content_designimage.id;


--
-- Name: content_designimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_designimage_id_seq', 1, false);


--
-- Name: content_housead; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_housead (
    id integer NOT NULL,
    page_id integer,
    name character varying(256),
    src character varying(300),
    url character varying(200),
    active boolean DEFAULT false NOT NULL,
    start date,
    "end" date
);


ALTER TABLE public.content_housead OWNER TO postgres;

--
-- Name: content_housead_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_housead_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_housead_id_seq OWNER TO postgres;

--
-- Name: content_housead_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_housead_id_seq OWNED BY content_housead.id;


--
-- Name: content_housead_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_housead_id_seq', 1, false);


--
-- Name: content_page; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_page (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    has_sidebar boolean DEFAULT false NOT NULL
);


ALTER TABLE public.content_page OWNER TO postgres;

--
-- Name: content_page_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_page_id_seq OWNER TO postgres;

--
-- Name: content_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_page_id_seq OWNED BY content_page.id;


--
-- Name: content_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_page_id_seq', 1, false);


--
-- Name: content_sidebarwidget; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_sidebarwidget (
    id integer NOT NULL,
    "order" integer DEFAULT 99999 NOT NULL,
    page_id integer,
    name character varying(256),
    template_id integer NOT NULL,
    CONSTRAINT content_sidebarwidget_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.content_sidebarwidget OWNER TO postgres;

--
-- Name: content_sidebarwidget_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_sidebarwidget_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_sidebarwidget_id_seq OWNER TO postgres;

--
-- Name: content_sidebarwidget_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_sidebarwidget_id_seq OWNED BY content_sidebarwidget.id;


--
-- Name: content_sidebarwidget_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_sidebarwidget_id_seq', 1, false);


--
-- Name: content_template; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE content_template (
    id integer NOT NULL,
    template character varying(64) NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.content_template OWNER TO postgres;

--
-- Name: content_template_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE content_template_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_template_id_seq OWNER TO postgres;

--
-- Name: content_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE content_template_id_seq OWNED BY content_template.id;


--
-- Name: content_template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('content_template_id_seq', 1, false);


--
-- Name: course_classtime; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_classtime (
    id integer NOT NULL,
    start timestamp with time zone NOT NULL,
    end_time time without time zone NOT NULL,
    session_id integer NOT NULL
);


ALTER TABLE public.course_classtime OWNER TO postgres;

--
-- Name: course_classtime_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_classtime_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_classtime_id_seq OWNER TO postgres;

--
-- Name: course_classtime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_classtime_id_seq OWNED BY course_classtime.id;


--
-- Name: course_classtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_classtime_id_seq', 3, true);


--
-- Name: course_course; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_course (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    src character varying(300)
);


ALTER TABLE public.course_course OWNER TO postgres;

--
-- Name: course_course_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_course_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_course_id_seq OWNER TO postgres;

--
-- Name: course_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_course_id_seq OWNED BY course_course.id;


--
-- Name: course_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_course_id_seq', 39, true);


--
-- Name: course_course_subjects; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_course_subjects (
    id integer NOT NULL,
    course_id integer NOT NULL,
    subject_id integer NOT NULL
);


ALTER TABLE public.course_course_subjects OWNER TO postgres;

--
-- Name: course_course_subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_course_subjects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_course_subjects_id_seq OWNER TO postgres;

--
-- Name: course_course_subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_course_subjects_id_seq OWNED BY course_course_subjects.id;


--
-- Name: course_course_subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_course_subjects_id_seq', 43, true);


--
-- Name: course_enrollment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_enrollment (
    id integer NOT NULL,
    user_id integer NOT NULL,
    session_id integer NOT NULL
);


ALTER TABLE public.course_enrollment OWNER TO postgres;

--
-- Name: course_enrollment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_enrollment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_enrollment_id_seq OWNER TO postgres;

--
-- Name: course_enrollment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_enrollment_id_seq OWNED BY course_enrollment.id;


--
-- Name: course_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_enrollment_id_seq', 1, false);


--
-- Name: course_section; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_section (
    id integer NOT NULL,
    course_id integer NOT NULL,
    term_id integer NOT NULL,
    fee integer,
    fee_notes character varying(256),
    description text,
    location_id integer DEFAULT 1 NOT NULL,
    src character varying(300),
    cancelled boolean DEFAULT false NOT NULL,
    max_students integer DEFAULT 40 NOT NULL
);


ALTER TABLE public.course_section OWNER TO postgres;

--
-- Name: course_section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_section_id_seq OWNER TO postgres;

--
-- Name: course_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_section_id_seq OWNED BY course_section.id;


--
-- Name: course_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_section_id_seq', 41, true);


--
-- Name: course_section_tools; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_section_tools (
    id integer NOT NULL,
    section_id integer NOT NULL,
    tool_id integer NOT NULL
);


ALTER TABLE public.course_section_tools OWNER TO postgres;

--
-- Name: course_section_tools_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_section_tools_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_section_tools_id_seq OWNER TO postgres;

--
-- Name: course_section_tools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_section_tools_id_seq OWNED BY course_section_tools.id;


--
-- Name: course_section_tools_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_section_tools_id_seq', 1, false);


--
-- Name: course_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_session (
    id integer NOT NULL,
    user_id integer NOT NULL,
    time_string character varying(128) NOT NULL,
    section_id integer NOT NULL
);


ALTER TABLE public.course_session OWNER TO postgres;

--
-- Name: course_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_session_id_seq OWNER TO postgres;

--
-- Name: course_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_session_id_seq OWNED BY course_session.id;


--
-- Name: course_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_session_id_seq', 2, true);


--
-- Name: course_subject; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_subject (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.course_subject OWNER TO postgres;

--
-- Name: course_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_subject_id_seq OWNER TO postgres;

--
-- Name: course_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_subject_id_seq OWNED BY course_subject.id;


--
-- Name: course_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_subject_id_seq', 10, true);


--
-- Name: course_term; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE course_term (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    start date NOT NULL,
    "end" date NOT NULL
);


ALTER TABLE public.course_term OWNER TO postgres;

--
-- Name: course_term_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE course_term_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.course_term_id_seq OWNER TO postgres;

--
-- Name: course_term_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE course_term_id_seq OWNED BY course_term.id;


--
-- Name: course_term_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('course_term_id_seq', 1, true);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 106, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 43, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: event_event; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE event_event (
    id integer NOT NULL,
    name character varying(128),
    starttime time without time zone NOT NULL,
    endtime time without time zone,
    location_id integer NOT NULL,
    schedule_id integer,
    description text NOT NULL,
    date date
);


ALTER TABLE public.event_event OWNER TO postgres;

--
-- Name: event_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE event_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.event_event_id_seq OWNER TO postgres;

--
-- Name: event_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE event_event_id_seq OWNED BY event_event.id;


--
-- Name: event_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('event_event_id_seq', 1, false);


--
-- Name: event_schedule; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE event_schedule (
    id integer NOT NULL,
    name character varying(128),
    date date NOT NULL
);


ALTER TABLE public.event_schedule OWNER TO postgres;

--
-- Name: event_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE event_schedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.event_schedule_id_seq OWNER TO postgres;

--
-- Name: event_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE event_schedule_id_seq OWNED BY event_schedule.id;


--
-- Name: event_schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('event_schedule_id_seq', 1, false);


--
-- Name: geo_city; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE geo_city (
    id integer NOT NULL,
    latlon character varying(500),
    name character varying(128) NOT NULL,
    state character varying(2) NOT NULL
);


ALTER TABLE public.geo_city OWNER TO postgres;

--
-- Name: geo_city_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE geo_city_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.geo_city_id_seq OWNER TO postgres;

--
-- Name: geo_city_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE geo_city_id_seq OWNED BY geo_city.id;


--
-- Name: geo_city_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('geo_city_id_seq', 1, true);


--
-- Name: geo_location; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE geo_location (
    id integer NOT NULL,
    latlon character varying(500),
    name character varying(128),
    address character varying(64),
    address2 character varying(64),
    city_id integer DEFAULT 1 NOT NULL,
    zip_code integer DEFAULT 77007 NOT NULL
);


ALTER TABLE public.geo_location OWNER TO postgres;

--
-- Name: geo_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE geo_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.geo_location_id_seq OWNER TO postgres;

--
-- Name: geo_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE geo_location_id_seq OWNED BY geo_location.id;


--
-- Name: geo_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('geo_location_id_seq', 1, true);


--
-- Name: membership_feature; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE membership_feature (
    id integer NOT NULL,
    membership_id integer NOT NULL,
    text character varying(128) NOT NULL,
    "order" integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.membership_feature OWNER TO postgres;

--
-- Name: membership_feature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE membership_feature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.membership_feature_id_seq OWNER TO postgres;

--
-- Name: membership_feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE membership_feature_id_seq OWNED BY membership_feature.id;


--
-- Name: membership_feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('membership_feature_id_seq', 1, false);


--
-- Name: membership_membership; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE membership_membership (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    notes character varying(256),
    "order" integer NOT NULL,
    monthly integer NOT NULL,
    yearly integer NOT NULL,
    student_rate integer
);


ALTER TABLE public.membership_membership OWNER TO postgres;

--
-- Name: membership_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE membership_membership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.membership_membership_id_seq OWNER TO postgres;

--
-- Name: membership_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE membership_membership_id_seq OWNED BY membership_membership.id;


--
-- Name: membership_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('membership_membership_id_seq', 1, false);


--
-- Name: membership_profile; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE membership_profile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    ghandle character varying(256),
    membership_id integer DEFAULT 1 NOT NULL,
    bio text,
    avatar character varying(300)
);


ALTER TABLE public.membership_profile OWNER TO postgres;

--
-- Name: membership_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE membership_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.membership_profile_id_seq OWNER TO postgres;

--
-- Name: membership_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE membership_profile_id_seq OWNED BY membership_profile.id;


--
-- Name: membership_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('membership_profile_id_seq', 1, false);


--
-- Name: membership_role; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE membership_role (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.membership_role OWNER TO postgres;

--
-- Name: membership_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE membership_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.membership_role_id_seq OWNER TO postgres;

--
-- Name: membership_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE membership_role_id_seq OWNED BY membership_role.id;


--
-- Name: membership_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('membership_role_id_seq', 1, false);


--
-- Name: membership_survey; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE membership_survey (
    id integer NOT NULL,
    user_id integer NOT NULL,
    reasons text NOT NULL,
    projects text NOT NULL,
    skills text NOT NULL,
    expertise text NOT NULL,
    questions text NOT NULL
);


ALTER TABLE public.membership_survey OWNER TO postgres;

--
-- Name: membership_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE membership_survey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.membership_survey_id_seq OWNER TO postgres;

--
-- Name: membership_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE membership_survey_id_seq OWNED BY membership_survey.id;


--
-- Name: membership_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('membership_survey_id_seq', 1, false);


--
-- Name: photo_photo; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE photo_photo (
    id integer NOT NULL,
    name character varying(512) NOT NULL,
    src character varying(300) NOT NULL,
    square_crop character varying(100),
    landscape_crop character varying(100),
    portrait_crop character varying(100)
);


ALTER TABLE public.photo_photo OWNER TO postgres;

--
-- Name: photo_photo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE photo_photo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.photo_photo_id_seq OWNER TO postgres;

--
-- Name: photo_photo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE photo_photo_id_seq OWNED BY photo_photo.id;


--
-- Name: photo_photo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('photo_photo_id_seq', 1, false);


--
-- Name: project_newsitem; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE project_newsitem (
    article_ptr_id integer NOT NULL
);


ALTER TABLE public.project_newsitem OWNER TO postgres;

--
-- Name: project_project; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE project_project (
    article_ptr_id integer NOT NULL
);


ALTER TABLE public.project_project OWNER TO postgres;

--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 21, true);


--
-- Name: thumbnail_kvstore; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE thumbnail_kvstore (
    key character varying(200) NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.thumbnail_kvstore OWNER TO postgres;

--
-- Name: tool_lab; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tool_lab (
    id integer NOT NULL,
    title character varying(128) NOT NULL,
    slug character varying(128),
    src character varying(300),
    "order" integer DEFAULT 9999 NOT NULL
);


ALTER TABLE public.tool_lab OWNER TO postgres;

--
-- Name: tool_lab_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tool_lab_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tool_lab_id_seq OWNER TO postgres;

--
-- Name: tool_lab_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tool_lab_id_seq OWNED BY tool_lab.id;


--
-- Name: tool_lab_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tool_lab_id_seq', 1, false);


--
-- Name: tool_tool; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tool_tool (
    id integer NOT NULL,
    title character varying(128) NOT NULL,
    slug character varying(128),
    lab_id integer NOT NULL,
    make character varying(64),
    model character varying(32),
    description text NOT NULL,
    "order" integer DEFAULT 9999 NOT NULL,
    thumbnail character varying(300)
);


ALTER TABLE public.tool_tool OWNER TO postgres;

--
-- Name: tool_tool_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tool_tool_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tool_tool_id_seq OWNER TO postgres;

--
-- Name: tool_tool_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tool_tool_id_seq OWNED BY tool_tool.id;


--
-- Name: tool_tool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tool_tool_id_seq', 1, false);


--
-- Name: tool_toollink; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tool_toollink (
    id integer NOT NULL,
    tool_id integer NOT NULL,
    "order" integer DEFAULT 9999 NOT NULL,
    title character varying(64) NOT NULL,
    url character varying(200) NOT NULL
);


ALTER TABLE public.tool_toollink OWNER TO postgres;

--
-- Name: tool_toollink_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tool_toollink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tool_toollink_id_seq OWNER TO postgres;

--
-- Name: tool_toollink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tool_toollink_id_seq OWNED BY tool_toollink.id;


--
-- Name: tool_toollink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tool_toollink_id_seq', 1, false);


--
-- Name: tool_toolphoto; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tool_toolphoto (
    id integer NOT NULL,
    "order" integer DEFAULT 9999 NOT NULL,
    tool_id integer NOT NULL,
    photo_id integer NOT NULL,
    caption_override character varying(512),
    CONSTRAINT tool_toolphoto_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.tool_toolphoto OWNER TO postgres;

--
-- Name: tool_toolphoto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tool_toolphoto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tool_toolphoto_id_seq OWNER TO postgres;

--
-- Name: tool_toolphoto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tool_toolphoto_id_seq OWNED BY tool_toolphoto.id;


--
-- Name: tool_toolphoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tool_toolphoto_id_seq', 1, false);


--
-- Name: tool_toolvideo; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tool_toolvideo (
    id integer NOT NULL,
    tool_id integer NOT NULL,
    "order" integer DEFAULT 9999 NOT NULL,
    title character varying(64) NOT NULL,
    embed_code text NOT NULL,
    thumbnail character varying(300),
    project_id integer
);


ALTER TABLE public.tool_toolvideo OWNER TO postgres;

--
-- Name: tool_toolvideo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tool_toolvideo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tool_toolvideo_id_seq OWNER TO postgres;

--
-- Name: tool_toolvideo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tool_toolvideo_id_seq OWNED BY tool_toolvideo.id;


--
-- Name: tool_toolvideo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tool_toolvideo_id_seq', 1, false);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article ALTER COLUMN id SET DEFAULT nextval('articles_article_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_followup_for ALTER COLUMN id SET DEFAULT nextval('articles_article_followup_for_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_related_articles ALTER COLUMN id SET DEFAULT nextval('articles_article_related_articles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_sites ALTER COLUMN id SET DEFAULT nextval('articles_article_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_tags ALTER COLUMN id SET DEFAULT nextval('articles_article_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_articlestatus ALTER COLUMN id SET DEFAULT nextval('articles_articlestatus_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_attachment ALTER COLUMN id SET DEFAULT nextval('articles_attachment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_tag ALTER COLUMN id SET DEFAULT nextval('articles_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_copy ALTER COLUMN id SET DEFAULT nextval('content_copy_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_designimage ALTER COLUMN id SET DEFAULT nextval('content_designimage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_housead ALTER COLUMN id SET DEFAULT nextval('content_housead_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_page ALTER COLUMN id SET DEFAULT nextval('content_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_sidebarwidget ALTER COLUMN id SET DEFAULT nextval('content_sidebarwidget_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_template ALTER COLUMN id SET DEFAULT nextval('content_template_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_classtime ALTER COLUMN id SET DEFAULT nextval('course_classtime_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_course ALTER COLUMN id SET DEFAULT nextval('course_course_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_course_subjects ALTER COLUMN id SET DEFAULT nextval('course_course_subjects_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_enrollment ALTER COLUMN id SET DEFAULT nextval('course_enrollment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section ALTER COLUMN id SET DEFAULT nextval('course_section_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section_tools ALTER COLUMN id SET DEFAULT nextval('course_section_tools_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_session ALTER COLUMN id SET DEFAULT nextval('course_session_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_subject ALTER COLUMN id SET DEFAULT nextval('course_subject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_term ALTER COLUMN id SET DEFAULT nextval('course_term_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY event_event ALTER COLUMN id SET DEFAULT nextval('event_event_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY event_schedule ALTER COLUMN id SET DEFAULT nextval('event_schedule_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geo_city ALTER COLUMN id SET DEFAULT nextval('geo_city_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geo_location ALTER COLUMN id SET DEFAULT nextval('geo_location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_feature ALTER COLUMN id SET DEFAULT nextval('membership_feature_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_membership ALTER COLUMN id SET DEFAULT nextval('membership_membership_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_profile ALTER COLUMN id SET DEFAULT nextval('membership_profile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_role ALTER COLUMN id SET DEFAULT nextval('membership_role_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_survey ALTER COLUMN id SET DEFAULT nextval('membership_survey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY photo_photo ALTER COLUMN id SET DEFAULT nextval('photo_photo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_lab ALTER COLUMN id SET DEFAULT nextval('tool_lab_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_tool ALTER COLUMN id SET DEFAULT nextval('tool_tool_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toollink ALTER COLUMN id SET DEFAULT nextval('tool_toollink_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolphoto ALTER COLUMN id SET DEFAULT nextval('tool_toolphoto_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolvideo ALTER COLUMN id SET DEFAULT nextval('tool_toolvideo_id_seq'::regclass);


--
-- Data for Name: articles_article; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_article (id, title, slug, status_id, author_id, keywords, description, markup, content, rendered_content, publish_date, expiration_date, is_active, login_required, use_addthis_button, addthis_use_author, addthis_username, auto_tag) FROM stdin;
\.


--
-- Data for Name: articles_article_followup_for; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_article_followup_for (id, from_article_id, to_article_id) FROM stdin;
\.


--
-- Data for Name: articles_article_related_articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_article_related_articles (id, from_article_id, to_article_id) FROM stdin;
\.


--
-- Data for Name: articles_article_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_article_sites (id, article_id, site_id) FROM stdin;
\.


--
-- Data for Name: articles_article_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_article_tags (id, article_id, tag_id) FROM stdin;
\.


--
-- Data for Name: articles_articlestatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_articlestatus (id, name, ordering, is_live) FROM stdin;
1	Draft	0	f
2	Finished	1	t
\.


--
-- Data for Name: articles_attachment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_attachment (id, article_id, attachment, caption) FROM stdin;
\.


--
-- Data for Name: articles_tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY articles_tag (id, name, slug) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add site	6	add_site
17	Can change site	6	change_site
18	Can delete site	6	delete_site
19	Can add log entry	7	add_logentry
20	Can change log entry	7	change_logentry
21	Can delete log entry	7	delete_logentry
22	Can add migration history	8	add_migrationhistory
23	Can change migration history	8	change_migrationhistory
24	Can delete migration history	8	delete_migrationhistory
25	Can add kv store	9	add_kvstore
26	Can change kv store	9	change_kvstore
27	Can delete kv store	9	delete_kvstore
28	Can add schedule	10	add_schedule
29	Can change schedule	10	change_schedule
30	Can delete schedule	10	delete_schedule
31	Can add event	11	add_event
32	Can change event	11	change_event
33	Can delete event	11	delete_event
34	Can add tag	12	add_tag
35	Can change tag	12	change_tag
36	Can delete tag	12	delete_tag
37	Can add article status	13	add_articlestatus
38	Can change article status	13	change_articlestatus
39	Can delete article status	13	delete_articlestatus
40	Can add article	14	add_article
41	Can change article	14	change_article
42	Can delete article	14	delete_article
43	Can add attachment	15	add_attachment
44	Can change attachment	15	change_attachment
45	Can delete attachment	15	delete_attachment
46	Can add photo	16	add_photo
47	Can change photo	16	change_photo
48	Can delete photo	16	delete_photo
49	Can add page	17	add_page
50	Can change page	17	change_page
51	Can delete page	17	delete_page
52	Can add copy	18	add_copy
53	Can change copy	18	change_copy
54	Can delete copy	18	delete_copy
55	Can add design image	19	add_designimage
56	Can change design image	19	change_designimage
57	Can delete design image	19	delete_designimage
58	Can add house ad	20	add_housead
59	Can change house ad	20	change_housead
60	Can delete house ad	20	delete_housead
61	Can add template	21	add_template
62	Can change template	21	change_template
63	Can delete template	21	delete_template
64	Can add side bar widget	22	add_sidebarwidget
65	Can change side bar widget	22	change_sidebarwidget
66	Can delete side bar widget	22	delete_sidebarwidget
67	Can add city	23	add_city
68	Can change city	23	change_city
69	Can delete city	23	delete_city
70	Can add location	24	add_location
71	Can change location	24	change_location
72	Can delete location	24	delete_location
73	Can add lab	25	add_lab
74	Can change lab	25	change_lab
75	Can delete lab	25	delete_lab
76	Can add tool	26	add_tool
77	Can change tool	26	change_tool
78	Can delete tool	26	delete_tool
79	Can add tool video	27	add_toolvideo
80	Can change tool video	27	change_toolvideo
81	Can delete tool video	27	delete_toolvideo
82	Can add tool link	28	add_toollink
83	Can change tool link	28	change_toollink
84	Can delete tool link	28	delete_toollink
85	Can add tool photo	29	add_toolphoto
86	Can change tool photo	29	change_toolphoto
87	Can delete tool photo	29	delete_toolphoto
88	Can add project	30	add_project
89	Can change project	30	change_project
90	Can delete project	30	delete_project
91	Can add news item	31	add_newsitem
92	Can change news item	31	change_newsitem
93	Can delete news item	31	delete_newsitem
94	Can add subject	32	add_subject
95	Can change subject	32	change_subject
96	Can delete subject	32	delete_subject
97	Can add term	33	add_term
98	Can change term	33	change_term
99	Can delete term	33	delete_term
100	Can add course	34	add_course
101	Can change course	34	change_course
102	Can delete course	34	delete_course
103	Can add section	35	add_section
104	Can change section	35	change_section
105	Can delete section	35	delete_section
106	Can add session	36	add_session
107	Can change session	36	change_session
108	Can delete session	36	delete_session
109	Can add class time	37	add_classtime
110	Can change class time	37	change_classtime
111	Can delete class time	37	delete_classtime
112	Can add enrollment	38	add_enrollment
113	Can change enrollment	38	change_enrollment
114	Can delete enrollment	38	delete_enrollment
115	Can add Membership Level	39	add_membership
116	Can change Membership Level	39	change_membership
117	Can delete Membership Level	39	delete_membership
118	Can add role	40	add_role
119	Can change role	40	change_role
120	Can delete role	40	delete_role
121	Can add feature	41	add_feature
122	Can change feature	41	change_feature
123	Can delete feature	41	delete_feature
124	Can add profile	42	add_profile
125	Can change profile	42	change_profile
126	Can delete profile	42	delete_profile
127	Can add survey	43	add_survey
128	Can change survey	43	change_survey
129	Can delete survey	43	delete_survey
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	kellyobrien	Kelley	Obrien	kel.m.obrien@gmail.com	pbkdf2_sha256$10000$0PLevXJU3Bz5$n8v9/D2DJ+vUUoO1TTf7KqqpSIC1c8YL6fdnpObB48g=	t	t	f	2012-08-19 17:53:17-04	2012-08-19 17:53:17-04
3	rtavk3	Roland	Kurnatowski	rtavk3@gmail.com	pbkdf2_sha256$10000$UtvKbiR3AX8j$waKUkZVccQtos9EtG0fQcpEEoJQVow2EDwz7TqhFyLM=	t	t	f	2012-08-19 17:54:21-04	2012-08-19 17:54:21-04
1	chriscauley	Chris	Cauley	chris@lablackey.com	pbkdf2_sha256$10000$7qu0dTpPqzbl$8WRgiUEcy+zJGxB3uwAe8L32jF8634dn3FkVQhK1Bkk=	t	t	t	2012-08-25 16:57:49.577993-04	2012-08-17 19:35:49-04
4	sandford	Mike	Sandford	sandford@ufl.edu	pbkdf2_sha256$10000$leNm81CWEc2o$PbKvb2oglnW1pyoTdZT5d/netHAyiL9j20AHHRtIjnk=	t	t	t	2012-08-25 16:58:05-04	2012-08-25 16:58:05-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: content_copy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_copy (id, page_id, name, context, text) FROM stdin;
\.


--
-- Data for Name: content_designimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_designimage (id, page_id, name, context, src) FROM stdin;
\.


--
-- Data for Name: content_housead; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_housead (id, page_id, name, src, url, active, start, "end") FROM stdin;
\.


--
-- Data for Name: content_page; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_page (id, name, has_sidebar) FROM stdin;
\.


--
-- Data for Name: content_sidebarwidget; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_sidebarwidget (id, "order", page_id, name, template_id) FROM stdin;
\.


--
-- Data for Name: content_template; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY content_template (id, template, name) FROM stdin;
\.


--
-- Data for Name: course_classtime; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_classtime (id, start, end_time, session_id) FROM stdin;
1	2012-08-23 13:00:00-04	04:00:00	1
2	2012-10-09 19:15:00-04	20:15:00	2
3	2012-10-10 19:15:00-04	20:15:00	2
\.


--
-- Data for Name: course_course; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_course (id, name, src) FROM stdin;
1	Python	
2	Brazing	
3	Welding I	
4	 Intro to Inventor (3-D Computer Aided Design) 	
5	Welding II	
6	Laser Cutting I	
7	Intro to PCB Layout with Eagle	
8	How to create your own PCBs	
9	Intro to 2D CAD/Drafting	
10	Oscilloscope Laboratory	
11	Stepper Motors	
12	Calculus for the Practical Person	
13	Intro to C Programming	
14	Wood Working	
15	Intro to HTML/CSS	
16	Intro to Programming: First Principles	
17	Intro to Django	
18	Automation for Non-Programmers: Ladder Logic	
19	Learning Javascript	
20	Intro to Arduino	
21	Advanced Arduino Development	
22	Intro to CNC	
23	Intro to Soldering	
24	Beginner iPhone/iPad Development	
25	Math for Game Development	
26	Android Programming	
27	DIY Multicopter	
28	Intro to Analog Circuits	
29	Intermediate Analog Circuits	
30	Bike Tech: Beginner Maintenance	
31	Bike Tech: Wheel Truing	
32	Bike Tech: Intermediate Maintenance	
33	Intro to Ruby	
34	Intro to Rails	
35	DIY Electric Vehicle Conversion	
36	Plasma Cutting	
37	3D Printing	
38	Introduction to Digital Signal Processing	
39	Intermediate iPhone/iPad Development	
\.


--
-- Data for Name: course_course_subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_course_subjects (id, course_id, subject_id) FROM stdin;
1	1	1
2	2	2
3	3	2
4	4	3
5	5	2
6	6	4
7	7	5
8	8	6
9	9	3
10	10	6
11	11	6
12	12	7
13	13	1
14	14	8
15	15	1
16	16	1
17	17	1
18	18	1
19	19	1
20	20	6
21	21	6
22	22	4
23	23	6
24	24	1
25	25	1
26	25	7
27	26	1
28	27	1
29	27	6
30	28	6
31	29	6
32	30	9
33	31	9
34	32	9
35	33	1
36	34	1
37	35	10
38	36	2
39	36	3
40	37	4
41	38	6
42	38	7
43	39	1
\.


--
-- Data for Name: course_enrollment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_enrollment (id, user_id, session_id) FROM stdin;
\.


--
-- Data for Name: course_section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_section (id, course_id, term_id, fee, fee_notes, description, location_id, src, cancelled, max_students) FROM stdin;
1	1	1	30	These are fee notes	There is a class description	1		f	40
2	2	1	55		Learn the basics of brazing safety and technique. 	1		f	40
3	3	1	75		Basics of MIG welding. How to weld safely and successfully. Emphasis on providing enough instruction and practice for the beginner to successfully complete a small project. Each Section Limited to 6 participants.	1		f	40
4	4	1	85			1		f	40
5	5	1	75		Continuation of Welding I. Emphasis on more advanced techniques with MIG / material selection / basic design for weldments. Intro to TIG time allowing. Each Section Limited to 6 participants.	1		f	40
6	6	1	35		This course will cover the basics of laser cutter principles and operation. Students will learn proper safety protocols for use of the laser cutter and also build a simple project to become familiar with techniques for construction using the laser cutter. Materials will be provided. 	1		f	40
7	36	1	40		This course will serve as an intro to anyone interested in using the CNC plasma cutter. The intro will include basic PlasmaCam software operation, material selection, parameter tuning, and safety considerations.	1		f	40
8	7	1	30			1		f	40
9	8	1	35		Want to make your own circuit boards for that project you've been building? This course will cover basic single sided pcb fabrication using the equipment available at the lab. Topics will include artwork generation, board exposure/developing/etching. Along with other techniques used in the creation of PCB's for prototyping and home production.	1		f	40
10	37	1	25		Students will learn basic and intermediate techniques of 3D CAD \r\n(Computer Aided Design&Drafting) and how it is used in rapid \r\nprototyping applications. The class will focus on the important concepts\r\n of designing parts that can be 3D printed or CNC machined. By the end \r\nof the course students will have designed and printed their own 3D \r\nparts.	1		f	40
11	9	1	25		This class will teach students basic drafting principals such as hand sketching parts, engineering drawing rules, measurements and tolerances. This course will also serve as an introduction to the world of 2D Drafting and a stepping stone to 3D CAD.	1		f	40
12	10	1	25		Oscilloscopes are well known as highly versatile instruments, but \r\nsome limited observations around TX/RX Labs indicate that many who try \r\nto use them do not have sufficient knowledge to use them effectively. \r\nThis course aims at correcting that.\r\nSpecific objectives are for students to learn:\r\n\r\n- Safety: potential hazards and how to avoid them.\r\n\r\n- What’s inside: general notions of how an oscilloscope produces a display (most details omitted).\r\n\r\n- Damage prevention: using an oscilloscope without damaging it or its accessories such as probes.\r\n\r\n- Probe adjustment: reducing the distortion of signals by probes.\r\n\r\n- Connection: minimizing the effect of probe attachment to circuits under test.\r\n\r\n- Single waveform display: setting controls for viewing and measuring various waveforms.\r\n\r\n- Multiple waveform display: observing and measuring the differences between two waveforms, including phase shift.\r\n\r\n- Interference reduction: arranging connections and controls to reduce \r\nnoise, power-line interference and other interfering signals.\r\n\r\n- Oscilloscope limitations: understand signal range limits, bandwidth effects, accuracy, etc.\r\n\r\n- Calibration checking.\r\n\r\n- Something about different types of oscilloscopes.\r\nThis is mostly a hands-on course, with some short lectures between \r\nlaboratory sessions. Laboratory exercises are designed to illustrate a \r\nrange of techniques and applications that is as broad as time permits. \r\nExamples are measurements of continuous signals such as sine waves, AM \r\nand FM signals, signals with pulses, and signals imbedded in random \r\nnoise; observation of characteristic curves of two-terminal devices such\r\n as diodes; and application of delayed triggering to observe brief \r\nsignal events. A handout will be available. Students may not be able to \r\nperform all of the laboratory exercises in the handout during class \r\ntime, but should be able to do them at TX/RX Labs outside of class.	1		f	40
13	38	1	25		As a partial answer to the question “What do I do with my signals after I get them into my computer,” this course deals with filtering, spectral analysis, and correlation of discrete-time signals. Specific topics include FIR and IIR filters, filter realization forms, design of filters, the fast Fourier transform (FFT), convolution by using the FFT. Prerequisites: a good understanding of the algebra and geometry of complex numbers and trigonometric functions. The course will use some concepts from differential and integral calculus.	1		f	40
14	11	1	25			1		f	40
15	12	1	25		Prerequisites: Students should have a good understanding of the algebra and geometry of complex numbers (this will be reviewed very briefly) and trigonometric functions. The course will use some concepts from differential and integral calculus.	1		f	40
16	13	1	35		This class is for beginning C programmers. It will cover most aspects of the C language including data types, structures, arrays, pointers, arithmetic, bitwise and logical operators, control flow, functions, and some parts of the standard C library for handling strings, i/o, and memory allocation. Students should bring a laptop with a working C compiler, as there will be some hands on exercises. C++ will *not* be covered. (Help will be provided prior to the class for those who need help getting a working c compiler on their computer)	1		f	40
17	14	1	35		Creating a small hardwood box using router, planer, bandsaw, handplane/jointer, table saw or miter saw	1		f	40
18	15	1	25		This short class will start with the structure of an HTML document and \r\ngo over the more common tags including the newer tags introduced in HTML\r\n 5. Next we will learn the basics of using Cascading Style Sheets(CSS) to formalize the layout and design of webpages.  Then we will briefly discuss how javascript and css interact with \r\nHTML to form a webpage.	1		f	40
20	16	1	35		This is a course for the absolute beginner at programming. Using the \r\nclean and simple Python language, this course will teach you how to \r\nteach yourself to use any programming language. If you have been trying \r\nto learn computer programming, but find it hard, take this course to \r\nlearn the “inner game” of programming that professionals and\r\nrockstar coders use to write programs. Edit, Test, Debug just like the pros do.\r\nThe format of this class will be an instructor assisted  self-paced \r\nstudy. Further class dates may be scheduled if participants need them.	1		f	40
21	17	1	40		Django is a powerful web framework written in python. After covering \r\ninstallation and basic configuration, this class will cover how to make a\r\n guestbook style web page. Then it will cover the the built in features \r\nof Django. Any additional time will be used to explore a few of the many\r\n 3rd party libraries available.\r\nPrerequisite: Knowledge of Python or any similar language (PHP, Ruby,\r\n Java, etc.), HTML, and some concept of relational databases is \r\nrequired.	1		f	40
22	18	1	70		Ladder Logic is a graphical paradigm that enables the development and maintainance of sophisticated control systems without knowledge of textual programming languages such as C, Basic, Assembler, etc.  Ladder Logic is inherently parallel and multi-tasking and frees the inventor from worrying about interrupts, stacks, and other advanced programming topics usually needed for real-time control.  Students will learn the basics of Ladder Logic diagramming and get an overview of advanced topics.   Basic electrical knowledge will be helpful.  Students should understand complete circuits. Basic Windows skills are required.  Students are encouraged to have an application in mind.	1		f	40
23	19	1	35			1		f	40
24	20	1	70		Participants will get a overview of the Arduino’s operation and features and then delve into hands-on development, learning how to use common sensors and program the Arduino platform. Arduinos and laptops will be provided. Space for this class is limited. 	1		f	40
25	21	1	40		Participants will go in-depth into the Arduino platform, covering topics such as interrupts, timers, peripheral modules, bit-banging, etc. This course will be a mix of hands on and lecture. Arduinos and laptops will be provided. Space for this class is limited.	1		f	40
26	22	1	30		This course will cover the basics of cnc operation using G-Code. Focusing mainly on 3 Axis Machining as our sandbox. Course participants will learn how to write and debug basic to intermediate G-Code. With the final products being run on the Lab’s Powerhawk mill.	1		f	40
27	23	1	30		Participants will learn the basic principles of soldering through a hands-on course. Includes an introduction to the soldering iron and its operation, basic through-hole soldering techniques, and many other topics. Participants will learn while assembling two simple project kits.	1		f	40
28	24	1	40		In this introduction to iPhone programming I will show you how to get started writing an app with Xcode and Objective-C. We will write a sample app that covers creating UI, User Interface navigation, displaying data in a tableview (iOS’s “list”), modal views, reading and writing to disk, displaying images and much more.	1		f	40
29	39	1	50			1		f	40
30	25	1	30		A Mac + Xcode installed will be required to code along. All source will be made available on Github.	1		f	40
31	26	1	45			1		f	40
32	27	1	180	Including the copter you take home	Workshop for learning the thory behind multicopters and their desighn+ students will build their own multicopters and maiden them.	1		f	40
34	29	1	25		Continuation of Intro to Analog Circuits. Includes a discussion of inductance, capacitance and other intermediate topics. This class will be half lecture with the remaining time being spent doing exercise based lab work.	1		f	40
35	30	1	15		Participants will learn the basics of repairing and maintaining their bikes. We will cover proper techniques for adjusting gears, brakes, bottom bracket and headset, as well as proper procedures for cleaning and doing emergency repairs.	1		f	40
36	31	1	15		Participants will learn how to true their own wheels along with identifying when wheels are out of alignment, a common occurrence that often goes unnoticed and leads to poor performance. Also we will cover hub adjustment, how to read spoke tension, and proper flat repair. Skills every cyclist should have!	1		f	40
37	32	1	15			1		f	40
38	33	1	1000			1		f	40
39	34	1	1000			1		f	40
40	35	1	25		Project Design, AC or DC, Lithium or Lead or ?	1		f	40
41	28	1	25		Introduction to current, voltage, resistance, Ohm’s Law, and Kirchhoff’s circuit laws. This class will be half lecture with the remaining time being spent doing exercise based lab work.	1		f	40
\.


--
-- Data for Name: course_section_tools; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_section_tools (id, section_id, tool_id) FROM stdin;
\.


--
-- Data for Name: course_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_session (id, user_id, time_string, section_id) FROM stdin;
1	1	arst	1
2	1	arst	18
\.


--
-- Data for Name: course_subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_subject (id, name) FROM stdin;
1	Programming
2	Metal Working
3	Drafting
4	Fqbrication
5	Misc
6	Electronics
7	Mathematics
8	Wood Working
9	Bicycles
10	Automotive
\.


--
-- Data for Name: course_term; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY course_term (id, name, start, "end") FROM stdin;
1	Fall 2012	2012-10-01	2012-12-15
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2012-08-17 19:49:27.459019-04	1	33	1	Fall 2012	1	
2	2012-08-17 19:50:46.483691-04	1	32	1	Subject object	1	
3	2012-08-17 19:50:54.69442-04	1	34	1	Python	1	
4	2012-08-17 19:51:51.852982-04	1	23	1	Houston, TX	1	
5	2012-08-17 19:52:20.051249-04	1	24	1	TX/RX Labs	1	
6	2012-08-17 19:52:29.416959-04	1	35	1	Python	1	
7	2012-08-18 22:33:23.726486-04	1	36	1	Session object	1	
8	2012-08-18 22:41:54.692166-04	1	36	1	Python - Fall 2012 (chriscauley)	2	Added class time "ClassTime object".
9	2012-08-18 22:43:02.252189-04	1	3	1	chriscauley	2	Changed password, first_name and last_name.
10	2012-08-18 22:53:47.801151-04	1	35	1	Python - Fall 2012	2	Changed fee_notes and description.
11	2012-08-19 16:44:15.555673-04	1	32	2	Metal Working	1	
12	2012-08-19 16:44:24.40641-04	1	34	2	Brazing	1	
13	2012-08-19 16:45:07.951258-04	1	35	2	Brazing - Fall 2012	1	
14	2012-08-19 16:45:40.793156-04	1	34	3	Welding I	1	
15	2012-08-19 16:46:21.238239-04	1	35	3	Welding I - Fall 2012	1	
16	2012-08-19 16:47:13.942243-04	1	32	3	Drafting	1	
17	2012-08-19 16:47:16.614664-04	1	34	4	 Intro to Inventor (3-D Computer Aided Design) 	1	
18	2012-08-19 16:47:54.632368-04	1	35	4	 Intro to Inventor (3-D Computer Aided Design)  - Fall 2012	1	
19	2012-08-19 16:48:24.928686-04	1	34	5	Welding II	1	
20	2012-08-19 16:48:59.273731-04	1	35	5	Welding II - Fall 2012	1	
21	2012-08-19 16:52:11.231581-04	1	32	4	Fqbrication	1	
22	2012-08-19 17:11:03.988414-04	1	34	6	Laser Cutting I	1	
23	2012-08-19 17:12:23.397369-04	1	32	5	Misc	1	
24	2012-08-19 17:12:25.824615-04	1	34	7	Intro to PCB Layout with Eagle	1	
25	2012-08-19 17:12:57.273099-04	1	32	6	Electronics	1	
26	2012-08-19 17:12:59.769891-04	1	34	8	How to create your own PCBs	1	
27	2012-08-19 17:13:13.985088-04	1	34	9	Intro to 2D CAD/Drafting	1	
28	2012-08-19 17:13:50.430677-04	1	34	10	Oscilloscope Laboratory	1	
29	2012-08-19 17:14:09.372793-04	1	34	11	Stepper Motors	1	
30	2012-08-19 17:14:34.858288-04	1	32	7	Mathematics	1	
31	2012-08-19 17:14:37.831353-04	1	34	12	Calculus for the Practical Person	1	
32	2012-08-19 17:14:52.260943-04	1	34	13	Intro to C Programming	1	
33	2012-08-19 17:15:09.368766-04	1	32	8	Wood Working	1	
34	2012-08-19 17:15:12.501106-04	1	34	14	Wood Working	1	
35	2012-08-19 17:15:23.136061-04	1	34	15	Intro to HTML/CSS	1	
36	2012-08-19 17:15:51.890659-04	1	34	16	Intro to Programming: First Principles	1	
37	2012-08-19 17:16:02.810702-04	1	34	17	Intro to Django	1	
38	2012-08-19 17:16:30.761039-04	1	34	18	Automation for Non-Programmers: Ladder Logic	1	
39	2012-08-19 17:16:42.161417-04	1	34	19	Learning Javascript	1	
40	2012-08-19 17:16:53.74178-04	1	34	20	Intro to Arduino	1	
41	2012-08-19 17:17:09.766672-04	1	34	21	Advanced Arduino Development	1	
42	2012-08-19 17:17:19.94184-04	1	34	22	Intro to CNC	1	
43	2012-08-19 17:17:39.392449-04	1	34	23	Intro to Soldering	1	
44	2012-08-19 17:17:56.85195-04	1	34	24	Beginner iPhone/iPad Development	1	
45	2012-08-19 17:18:16.267076-04	1	34	25	Math for Game Development	1	
46	2012-08-19 17:18:31.931894-04	1	34	26	Android Programming	1	
47	2012-08-19 17:18:54.518269-04	1	34	27	DIY Multicopter	1	
48	2012-08-19 17:19:07.677962-04	1	34	28	Intro to Analog Circuits	1	
49	2012-08-19 17:19:16.052396-04	1	34	29	Intermediate Analog Circuits	1	
50	2012-08-19 17:19:46.630505-04	1	32	9	Bicycles	1	
51	2012-08-19 17:19:51.262856-04	1	34	30	Bike Tech: Beginner Maintenance	1	
52	2012-08-19 17:20:03.352588-04	1	34	31	Bike Tech: Wheel Truing	1	
53	2012-08-19 17:20:28.567997-04	1	34	32	Bike Tech: Intermediate Maintenance	1	
54	2012-08-19 17:20:39.31821-04	1	34	33	Intro to Ruby	1	
55	2012-08-19 17:20:48.275781-04	1	34	34	Intro to Rails	1	
56	2012-08-19 17:21:10.796307-04	1	32	10	Automotive	1	
57	2012-08-19 17:21:13.62368-04	1	34	35	DIY Electric Vehicle Conversion	1	
58	2012-08-19 17:23:38.537407-04	1	35	6	Laser Cutting I - Fall 2012	1	
59	2012-08-19 17:26:55.973075-04	1	34	36	Plasma Cutting	1	
60	2012-08-19 17:27:11.833382-04	1	35	7	Plasma Cutting - Fall 2012	1	
61	2012-08-19 17:27:35.969533-04	1	35	8	Intro to PCB Layout with Eagle - Fall 2012	1	
62	2012-08-19 17:28:05.179378-04	1	35	9	How to create your own PCBs - Fall 2012	1	
63	2012-08-19 17:32:59.85996-04	1	34	37	3D Printing	1	
64	2012-08-19 17:33:11.387089-04	1	35	10	3D Printing - Fall 2012	1	
65	2012-08-19 17:33:30.40681-04	1	35	11	Intro to 2D CAD/Drafting - Fall 2012	1	
66	2012-08-19 17:35:23.568234-04	1	35	12	Oscilloscope Laboratory - Fall 2012	1	
67	2012-08-19 17:36:01.780881-04	1	34	38	Introduction to Digital Signal Processing	1	
68	2012-08-19 17:36:16.088298-04	1	35	13	Introduction to Digital Signal Processing - Fall 2012	1	
69	2012-08-19 17:36:42.198245-04	1	35	14	Stepper Motors - Fall 2012	1	
70	2012-08-19 17:37:12.813304-04	1	35	15	Calculus for the Practical Person - Fall 2012	1	
71	2012-08-19 17:37:28.383097-04	1	35	16	Intro to C Programming - Fall 2012	1	
72	2012-08-19 17:37:58.918256-04	1	35	17	Wood Working - Fall 2012	1	
73	2012-08-19 17:38:34.18944-04	1	35	18	Intro to HTML/CSS - Fall 2012	1	
74	2012-08-19 17:38:34.313856-04	1	35	19	Intro to HTML/CSS - Fall 2012	1	
75	2012-08-19 17:39:02.370002-04	1	35	20	Intro to Programming: First Principles - Fall 2012	1	
76	2012-08-19 17:39:44.426798-04	1	35	21	Intro to Django - Fall 2012	1	
77	2012-08-19 17:40:18.769937-04	1	35	22	Automation for Non-Programmers: Ladder Logic - Fall 2012	1	
78	2012-08-19 17:40:41.929922-04	1	35	23	Learning Javascript - Fall 2012	1	
79	2012-08-19 17:41:12.27038-04	1	35	24	Intro to Arduino - Fall 2012	1	
80	2012-08-19 17:41:48.894987-04	1	35	25	Advanced Arduino Development - Fall 2012	1	
81	2012-08-19 17:42:09.591151-04	1	35	26	Intro to CNC - Fall 2012	1	
82	2012-08-19 17:42:34.376358-04	1	35	27	Intro to Soldering - Fall 2012	1	
83	2012-08-19 17:42:51.976066-04	1	35	28	Beginner iPhone/iPad Development - Fall 2012	1	
84	2012-08-19 17:43:23.098227-04	1	34	39	Intermediate iPhone/iPad Development	1	
85	2012-08-19 17:43:32.736905-04	1	35	29	Intermediate iPhone/iPad Development - Fall 2012	1	
86	2012-08-19 17:44:04.771824-04	1	35	30	Math for Game Development - Fall 2012	1	
87	2012-08-19 17:44:21.666134-04	1	35	31	Android Programming - Fall 2012	1	
88	2012-08-19 17:45:00.276814-04	1	35	32	DIY Multicopter - Fall 2012	1	
89	2012-08-19 17:45:17.232549-04	1	35	33	Intermediate Analog Circuits - Fall 2012	1	
90	2012-08-19 17:45:47.292214-04	1	35	34	Intermediate Analog Circuits - Fall 2012	1	
91	2012-08-19 17:46:15.297466-04	1	35	35	Bike Tech: Beginner Maintenance - Fall 2012	1	
92	2012-08-19 17:46:33.527574-04	1	35	36	Bike Tech: Wheel Truing - Fall 2012	1	
93	2012-08-19 17:49:07.294029-04	1	35	37	Bike Tech: Intermediate Maintenance - Fall 2012	1	
94	2012-08-19 17:49:47.409135-04	1	35	38	Intro to Ruby - Fall 2012	1	
95	2012-08-19 17:49:58.874336-04	1	35	39	Intro to Rails - Fall 2012	1	
96	2012-08-19 17:50:19.064248-04	1	35	40	DIY Electric Vehicle Conversion - Fall 2012	1	
97	2012-08-19 17:53:17.969146-04	1	3	2	kellyobrien	1	
98	2012-08-19 17:53:39.18048-04	1	3	2	kellyobrien	2	Changed password, first_name, last_name, email and is_staff.
99	2012-08-19 17:54:21.43058-04	1	3	3	rtavk3	1	
100	2012-08-19 17:55:01.800015-04	1	3	3	rtavk3	2	Changed password, first_name, last_name, email and is_staff.
101	2012-08-19 18:11:05.694652-04	1	36	2	Intro to HTML/CSS - Fall 2012 (chriscauley)	1	
102	2012-08-19 18:15:08.071058-04	1	35	19	Intro to HTML/CSS - Fall 2012	3	
103	2012-08-19 18:15:35.849527-04	1	35	41	Intro to Analog Circuits - Fall 2012	1	
104	2012-08-19 18:16:15.042932-04	1	35	33	Intermediate Analog Circuits - Fall 2012	3	
105	2012-08-25 16:58:05.468335-04	1	3	4	sandford	1	
106	2012-08-25 16:58:43.179492-04	1	3	4	sandford	2	Changed password, first_name, last_name, email, is_staff and is_superuser.
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	content type	contenttypes	contenttype
5	session	sessions	session
6	site	sites	site
7	log entry	admin	logentry
8	migration history	south	migrationhistory
9	kv store	thumbnail	kvstore
10	schedule	event	schedule
11	event	event	event
12	tag	articles	tag
13	article status	articles	articlestatus
14	article	articles	article
15	attachment	articles	attachment
16	photo	photo	photo
17	page	content	page
18	copy	content	copy
19	design image	content	designimage
20	house ad	content	housead
21	template	content	template
22	side bar widget	content	sidebarwidget
23	city	geo	city
24	location	geo	location
25	lab	tool	lab
26	tool	tool	tool
27	tool video	tool	toolvideo
28	tool link	tool	toollink
29	tool photo	tool	toolphoto
30	project	project	project
31	news item	project	newsitem
32	subject	course	subject
33	term	course	term
34	course	course	course
35	section	course	section
36	session	course	session
37	class time	course	classtime
38	enrollment	course	enrollment
39	Membership Level	membership	membership
40	role	membership	role
41	feature	membership	feature
42	profile	membership	profile
43	survey	membership	survey
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
2f5fac07521742e5a7ff1a901089352f	NDI5ZTEwOGZhM2YwZDNhZGQ5MTA5NDQ0MWIwYTQ3MjU5ODdjYzg0NjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-08-31 19:49:01.746589-04
ea9903115bd879604a424699a52da98a	NDI5ZTEwOGZhM2YwZDNhZGQ5MTA5NDQ0MWIwYTQ3MjU5ODdjYzg0NjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-03 21:06:55.439671-04
2d5c3bd43ffbc289d5b6b39aa4136e42	NDI5ZTEwOGZhM2YwZDNhZGQ5MTA5NDQ0MWIwYTQ3MjU5ODdjYzg0NjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-08 16:57:49.613687-04
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: event_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY event_event (id, name, starttime, endtime, location_id, schedule_id, description, date) FROM stdin;
\.


--
-- Data for Name: event_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY event_schedule (id, name, date) FROM stdin;
\.


--
-- Data for Name: geo_city; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY geo_city (id, latlon, name, state) FROM stdin;
1	29.76019,-95.36932999999999	Houston	TX
\.


--
-- Data for Name: geo_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY geo_location (id, latlon, name, address, address2, city_id, zip_code) FROM stdin;
1	29.758103683550853,-95.34907395751952	TX/RX Labs	2020 Commerce Street		1	77002
\.


--
-- Data for Name: membership_feature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY membership_feature (id, membership_id, text, "order") FROM stdin;
\.


--
-- Data for Name: membership_membership; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY membership_membership (id, name, notes, "order", monthly, yearly, student_rate) FROM stdin;
\.


--
-- Data for Name: membership_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY membership_profile (id, user_id, ghandle, membership_id, bio, avatar) FROM stdin;
\.


--
-- Data for Name: membership_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY membership_role (id, name) FROM stdin;
\.


--
-- Data for Name: membership_survey; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY membership_survey (id, user_id, reasons, projects, skills, expertise, questions) FROM stdin;
\.


--
-- Data for Name: photo_photo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY photo_photo (id, name, src, square_crop, landscape_crop, portrait_crop) FROM stdin;
\.


--
-- Data for Name: project_newsitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY project_newsitem (article_ptr_id) FROM stdin;
\.


--
-- Data for Name: project_project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY project_project (article_ptr_id) FROM stdin;
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	articles	0001_initial	2012-08-17 19:37:07.894718-04
2	articles	0002_auto__add_field_article_auto_tag	2012-08-17 19:37:07.975908-04
3	articles	0003_auto__add_field_tag_slug	2012-08-17 19:37:08.039039-04
4	articles	0004_set_tag_slugs	2012-08-17 19:37:08.062848-04
5	articles	0005_make_slugs_unique	2012-08-17 19:37:08.125894-04
6	photo	0001_initial	2012-08-17 19:37:08.1875-04
7	photo	0002_auto__add_field_photo_square_crop__add_field_photo_landscape_crop__add	2012-08-17 19:37:08.276827-04
8	content	0001_initial	2012-08-17 19:37:08.407999-04
9	geo	0001_initial	2012-08-17 19:37:08.527887-04
10	profile	0001_initial	2012-08-17 19:37:08.592218-04
11	profile	0002_auto__del_profile	2012-08-17 19:37:08.599111-04
12	event	0001_initial	2012-08-17 19:37:08.670209-04
13	event	0002_auto__add_field_event_description	2012-08-17 19:37:08.715314-04
14	event	0003_auto__chg_field_event_starttime__chg_field_event_endtime	2012-08-17 19:37:08.815039-04
15	event	0004_auto__add_field_event_date__del_field_schedule_starttime__del_field_sc	2012-08-17 19:37:08.859276-04
16	project	0001_initial	2012-08-17 19:37:16.231554-04
17	tool	0001_initial	2012-08-17 19:37:21.186615-04
18	course	0001_initial	2012-08-17 19:37:21.430551-04
19	membership	0001_initial	2012-08-17 19:37:21.615839-04
20	course	0002_auto__add_field_session_section	2012-08-18 22:31:11.941545-04
21	course	0003_auto__add_field_classtime_session__del_field_enrollment_section__add_f	2012-08-18 22:37:08.877551-04
\.


--
-- Data for Name: thumbnail_kvstore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY thumbnail_kvstore (key, value) FROM stdin;
\.


--
-- Data for Name: tool_lab; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tool_lab (id, title, slug, src, "order") FROM stdin;
\.


--
-- Data for Name: tool_tool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tool_tool (id, title, slug, lab_id, make, model, description, "order", thumbnail) FROM stdin;
\.


--
-- Data for Name: tool_toollink; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tool_toollink (id, tool_id, "order", title, url) FROM stdin;
\.


--
-- Data for Name: tool_toolphoto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tool_toolphoto (id, "order", tool_id, photo_id, caption_override) FROM stdin;
\.


--
-- Data for Name: tool_toolvideo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tool_toolvideo (id, tool_id, "order", title, embed_code, thumbnail, project_id) FROM stdin;
\.


--
-- Name: articles_article_followup_for_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_followup_for
    ADD CONSTRAINT articles_article_followup_for_pkey PRIMARY KEY (id);


--
-- Name: articles_article_followup_from_article_id_48ae772720da3481_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_followup_for
    ADD CONSTRAINT articles_article_followup_from_article_id_48ae772720da3481_uniq UNIQUE (from_article_id, to_article_id);


--
-- Name: articles_article_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article
    ADD CONSTRAINT articles_article_pkey PRIMARY KEY (id);


--
-- Name: articles_article_related__from_article_id_242e5577cb2613a2_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_related_articles
    ADD CONSTRAINT articles_article_related__from_article_id_242e5577cb2613a2_uniq UNIQUE (from_article_id, to_article_id);


--
-- Name: articles_article_related_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_related_articles
    ADD CONSTRAINT articles_article_related_articles_pkey PRIMARY KEY (id);


--
-- Name: articles_article_sites_article_id_547ed8e6249e8be5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_sites
    ADD CONSTRAINT articles_article_sites_article_id_547ed8e6249e8be5_uniq UNIQUE (article_id, site_id);


--
-- Name: articles_article_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_sites
    ADD CONSTRAINT articles_article_sites_pkey PRIMARY KEY (id);


--
-- Name: articles_article_tags_article_id_5919f2cbef69a9dd_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_tags
    ADD CONSTRAINT articles_article_tags_article_id_5919f2cbef69a9dd_uniq UNIQUE (article_id, tag_id);


--
-- Name: articles_article_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_article_tags
    ADD CONSTRAINT articles_article_tags_pkey PRIMARY KEY (id);


--
-- Name: articles_articlestatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_articlestatus
    ADD CONSTRAINT articles_articlestatus_pkey PRIMARY KEY (id);


--
-- Name: articles_attachment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_attachment
    ADD CONSTRAINT articles_attachment_pkey PRIMARY KEY (id);


--
-- Name: articles_tag_a951d5d6; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_tag
    ADD CONSTRAINT articles_tag_a951d5d6 UNIQUE (slug);


--
-- Name: articles_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_tag
    ADD CONSTRAINT articles_tag_name_key UNIQUE (name);


--
-- Name: articles_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY articles_tag
    ADD CONSTRAINT articles_tag_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: content_copy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_copy
    ADD CONSTRAINT content_copy_pkey PRIMARY KEY (id);


--
-- Name: content_designimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_designimage
    ADD CONSTRAINT content_designimage_pkey PRIMARY KEY (id);


--
-- Name: content_housead_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_housead
    ADD CONSTRAINT content_housead_pkey PRIMARY KEY (id);


--
-- Name: content_page_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_page
    ADD CONSTRAINT content_page_pkey PRIMARY KEY (id);


--
-- Name: content_sidebarwidget_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_sidebarwidget
    ADD CONSTRAINT content_sidebarwidget_pkey PRIMARY KEY (id);


--
-- Name: content_template_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY content_template
    ADD CONSTRAINT content_template_pkey PRIMARY KEY (id);


--
-- Name: course_classtime_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_classtime
    ADD CONSTRAINT course_classtime_pkey PRIMARY KEY (id);


--
-- Name: course_course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_course
    ADD CONSTRAINT course_course_pkey PRIMARY KEY (id);


--
-- Name: course_course_subjects_course_id_ea4f66d546d453b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_course_subjects
    ADD CONSTRAINT course_course_subjects_course_id_ea4f66d546d453b_uniq UNIQUE (course_id, subject_id);


--
-- Name: course_course_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_course_subjects
    ADD CONSTRAINT course_course_subjects_pkey PRIMARY KEY (id);


--
-- Name: course_enrollment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_enrollment
    ADD CONSTRAINT course_enrollment_pkey PRIMARY KEY (id);


--
-- Name: course_section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_section
    ADD CONSTRAINT course_section_pkey PRIMARY KEY (id);


--
-- Name: course_section_tools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_section_tools
    ADD CONSTRAINT course_section_tools_pkey PRIMARY KEY (id);


--
-- Name: course_section_tools_section_id_62c6879bd676cbeb_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_section_tools
    ADD CONSTRAINT course_section_tools_section_id_62c6879bd676cbeb_uniq UNIQUE (section_id, tool_id);


--
-- Name: course_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_session
    ADD CONSTRAINT course_session_pkey PRIMARY KEY (id);


--
-- Name: course_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_subject
    ADD CONSTRAINT course_subject_pkey PRIMARY KEY (id);


--
-- Name: course_term_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY course_term
    ADD CONSTRAINT course_term_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: event_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY event_event
    ADD CONSTRAINT event_event_pkey PRIMARY KEY (id);


--
-- Name: event_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY event_schedule
    ADD CONSTRAINT event_schedule_pkey PRIMARY KEY (id);


--
-- Name: geo_city_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY geo_city
    ADD CONSTRAINT geo_city_pkey PRIMARY KEY (id);


--
-- Name: geo_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY geo_location
    ADD CONSTRAINT geo_location_pkey PRIMARY KEY (id);


--
-- Name: membership_feature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_feature
    ADD CONSTRAINT membership_feature_pkey PRIMARY KEY (id);


--
-- Name: membership_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_membership
    ADD CONSTRAINT membership_membership_pkey PRIMARY KEY (id);


--
-- Name: membership_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_profile
    ADD CONSTRAINT membership_profile_pkey PRIMARY KEY (id);


--
-- Name: membership_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_profile
    ADD CONSTRAINT membership_profile_user_id_key UNIQUE (user_id);


--
-- Name: membership_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_role
    ADD CONSTRAINT membership_role_pkey PRIMARY KEY (id);


--
-- Name: membership_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_survey
    ADD CONSTRAINT membership_survey_pkey PRIMARY KEY (id);


--
-- Name: membership_survey_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY membership_survey
    ADD CONSTRAINT membership_survey_user_id_key UNIQUE (user_id);


--
-- Name: photo_photo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY photo_photo
    ADD CONSTRAINT photo_photo_pkey PRIMARY KEY (id);


--
-- Name: project_newsitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY project_newsitem
    ADD CONSTRAINT project_newsitem_pkey PRIMARY KEY (article_ptr_id);


--
-- Name: project_project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY project_project
    ADD CONSTRAINT project_project_pkey PRIMARY KEY (article_ptr_id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: thumbnail_kvstore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY thumbnail_kvstore
    ADD CONSTRAINT thumbnail_kvstore_pkey PRIMARY KEY (key);


--
-- Name: tool_lab_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tool_lab
    ADD CONSTRAINT tool_lab_pkey PRIMARY KEY (id);


--
-- Name: tool_tool_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tool_tool
    ADD CONSTRAINT tool_tool_pkey PRIMARY KEY (id);


--
-- Name: tool_toollink_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tool_toollink
    ADD CONSTRAINT tool_toollink_pkey PRIMARY KEY (id);


--
-- Name: tool_toolphoto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tool_toolphoto
    ADD CONSTRAINT tool_toolphoto_pkey PRIMARY KEY (id);


--
-- Name: tool_toolvideo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tool_toolvideo
    ADD CONSTRAINT tool_toolvideo_pkey PRIMARY KEY (id);


--
-- Name: articles_article_author_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_author_id ON articles_article USING btree (author_id);


--
-- Name: articles_article_followup_for_from_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_followup_for_from_article_id ON articles_article_followup_for USING btree (from_article_id);


--
-- Name: articles_article_followup_for_to_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_followup_for_to_article_id ON articles_article_followup_for USING btree (to_article_id);


--
-- Name: articles_article_related_articles_from_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_related_articles_from_article_id ON articles_article_related_articles USING btree (from_article_id);


--
-- Name: articles_article_related_articles_to_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_related_articles_to_article_id ON articles_article_related_articles USING btree (to_article_id);


--
-- Name: articles_article_sites_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_sites_article_id ON articles_article_sites USING btree (article_id);


--
-- Name: articles_article_sites_site_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_sites_site_id ON articles_article_sites USING btree (site_id);


--
-- Name: articles_article_slug; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_slug ON articles_article USING btree (slug);


--
-- Name: articles_article_slug_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_slug_like ON articles_article USING btree (slug varchar_pattern_ops);


--
-- Name: articles_article_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_status_id ON articles_article USING btree (status_id);


--
-- Name: articles_article_tags_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_tags_article_id ON articles_article_tags USING btree (article_id);


--
-- Name: articles_article_tags_tag_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_article_tags_tag_id ON articles_article_tags USING btree (tag_id);


--
-- Name: articles_attachment_article_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX articles_attachment_article_id ON articles_attachment USING btree (article_id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: content_copy_page_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX content_copy_page_id ON content_copy USING btree (page_id);


--
-- Name: content_designimage_page_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX content_designimage_page_id ON content_designimage USING btree (page_id);


--
-- Name: content_housead_page_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX content_housead_page_id ON content_housead USING btree (page_id);


--
-- Name: content_sidebarwidget_page_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX content_sidebarwidget_page_id ON content_sidebarwidget USING btree (page_id);


--
-- Name: content_sidebarwidget_template_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX content_sidebarwidget_template_id ON content_sidebarwidget USING btree (template_id);


--
-- Name: course_classtime_session_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_classtime_session_id ON course_classtime USING btree (session_id);


--
-- Name: course_course_subjects_course_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_course_subjects_course_id ON course_course_subjects USING btree (course_id);


--
-- Name: course_course_subjects_subject_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_course_subjects_subject_id ON course_course_subjects USING btree (subject_id);


--
-- Name: course_enrollment_session_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_enrollment_session_id ON course_enrollment USING btree (session_id);


--
-- Name: course_enrollment_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_enrollment_user_id ON course_enrollment USING btree (user_id);


--
-- Name: course_section_course_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_section_course_id ON course_section USING btree (course_id);


--
-- Name: course_section_location_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_section_location_id ON course_section USING btree (location_id);


--
-- Name: course_section_term_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_section_term_id ON course_section USING btree (term_id);


--
-- Name: course_section_tools_section_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_section_tools_section_id ON course_section_tools USING btree (section_id);


--
-- Name: course_section_tools_tool_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_section_tools_tool_id ON course_section_tools USING btree (tool_id);


--
-- Name: course_session_section_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_session_section_id ON course_session USING btree (section_id);


--
-- Name: course_session_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX course_session_user_id ON course_session USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: event_event_location_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX event_event_location_id ON event_event USING btree (location_id);


--
-- Name: event_event_schedule_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX event_event_schedule_id ON event_event USING btree (schedule_id);


--
-- Name: geo_location_city_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX geo_location_city_id ON geo_location USING btree (city_id);


--
-- Name: membership_feature_membership_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX membership_feature_membership_id ON membership_feature USING btree (membership_id);


--
-- Name: membership_profile_membership_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX membership_profile_membership_id ON membership_profile USING btree (membership_id);


--
-- Name: tool_tool_lab_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_tool_lab_id ON tool_tool USING btree (lab_id);


--
-- Name: tool_toollink_tool_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_toollink_tool_id ON tool_toollink USING btree (tool_id);


--
-- Name: tool_toolphoto_photo_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_toolphoto_photo_id ON tool_toolphoto USING btree (photo_id);


--
-- Name: tool_toolphoto_tool_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_toolphoto_tool_id ON tool_toolphoto USING btree (tool_id);


--
-- Name: tool_toolvideo_project_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_toolvideo_project_id ON tool_toolvideo USING btree (project_id);


--
-- Name: tool_toolvideo_tool_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX tool_toolvideo_tool_id ON tool_toolvideo USING btree (tool_id);


--
-- Name: article_id_refs_id_2baf76ee9a7bb474; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_sites
    ADD CONSTRAINT article_id_refs_id_2baf76ee9a7bb474 FOREIGN KEY (article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: article_id_refs_id_6d7bc685fd7e477a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_tags
    ADD CONSTRAINT article_id_refs_id_6d7bc685fd7e477a FOREIGN KEY (article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: article_id_refs_id_7f652d00bbffbc2d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_attachment
    ADD CONSTRAINT article_id_refs_id_7f652d00bbffbc2d FOREIGN KEY (article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: article_ptr_id_refs_id_1b77bf83a3787085; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_newsitem
    ADD CONSTRAINT article_ptr_id_refs_id_1b77bf83a3787085 FOREIGN KEY (article_ptr_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: article_ptr_id_refs_id_47aaaea03498927f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_project
    ADD CONSTRAINT article_ptr_id_refs_id_47aaaea03498927f FOREIGN KEY (article_ptr_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: author_id_refs_id_6612f51921e48f8a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article
    ADD CONSTRAINT author_id_refs_id_6612f51921e48f8a FOREIGN KEY (author_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: city_id_refs_id_32a10fe20904a915; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geo_location
    ADD CONSTRAINT city_id_refs_id_32a10fe20904a915 FOREIGN KEY (city_id) REFERENCES geo_city(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: course_id_refs_id_2d98bbaac42bcea; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section
    ADD CONSTRAINT course_id_refs_id_2d98bbaac42bcea FOREIGN KEY (course_id) REFERENCES course_course(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: course_id_refs_id_5ec75a474ca7272; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_course_subjects
    ADD CONSTRAINT course_id_refs_id_5ec75a474ca7272 FOREIGN KEY (course_id) REFERENCES course_course(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: from_article_id_refs_id_1bf7090e87599599; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_followup_for
    ADD CONSTRAINT from_article_id_refs_id_1bf7090e87599599 FOREIGN KEY (from_article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: from_article_id_refs_id_4fe177d23bb1e638; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_related_articles
    ADD CONSTRAINT from_article_id_refs_id_4fe177d23bb1e638 FOREIGN KEY (from_article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lab_id_refs_id_4c25692e86bdfc1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_tool
    ADD CONSTRAINT lab_id_refs_id_4c25692e86bdfc1 FOREIGN KEY (lab_id) REFERENCES tool_lab(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: location_id_refs_id_3185da004f1a0e2f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section
    ADD CONSTRAINT location_id_refs_id_3185da004f1a0e2f FOREIGN KEY (location_id) REFERENCES geo_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: location_id_refs_id_6d5d02e3a2b0e3c8; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY event_event
    ADD CONSTRAINT location_id_refs_id_6d5d02e3a2b0e3c8 FOREIGN KEY (location_id) REFERENCES geo_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_id_refs_id_287f19ef0eafece0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_feature
    ADD CONSTRAINT membership_id_refs_id_287f19ef0eafece0 FOREIGN KEY (membership_id) REFERENCES membership_membership(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_id_refs_id_4d6205fbddb3cf17; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_profile
    ADD CONSTRAINT membership_id_refs_id_4d6205fbddb3cf17 FOREIGN KEY (membership_id) REFERENCES membership_membership(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: page_id_refs_id_183f54b9c1be68e1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_copy
    ADD CONSTRAINT page_id_refs_id_183f54b9c1be68e1 FOREIGN KEY (page_id) REFERENCES content_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: page_id_refs_id_19d25ae5532a4168; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_housead
    ADD CONSTRAINT page_id_refs_id_19d25ae5532a4168 FOREIGN KEY (page_id) REFERENCES content_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: page_id_refs_id_4d4320f8ca1adcd6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_designimage
    ADD CONSTRAINT page_id_refs_id_4d4320f8ca1adcd6 FOREIGN KEY (page_id) REFERENCES content_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: page_id_refs_id_52792764d34f97df; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_sidebarwidget
    ADD CONSTRAINT page_id_refs_id_52792764d34f97df FOREIGN KEY (page_id) REFERENCES content_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: photo_id_refs_id_2b9577843ecf689e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolphoto
    ADD CONSTRAINT photo_id_refs_id_2b9577843ecf689e FOREIGN KEY (photo_id) REFERENCES photo_photo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_id_refs_article_ptr_id_29a176ff600b122b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolvideo
    ADD CONSTRAINT project_id_refs_article_ptr_id_29a176ff600b122b FOREIGN KEY (project_id) REFERENCES project_project(article_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schedule_id_refs_id_f061003840c2403; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY event_event
    ADD CONSTRAINT schedule_id_refs_id_f061003840c2403 FOREIGN KEY (schedule_id) REFERENCES event_schedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: section_id_refs_id_4c59311d8be60f1f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section_tools
    ADD CONSTRAINT section_id_refs_id_4c59311d8be60f1f FOREIGN KEY (section_id) REFERENCES course_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: section_id_refs_id_73fa915397e1f61c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_session
    ADD CONSTRAINT section_id_refs_id_73fa915397e1f61c FOREIGN KEY (section_id) REFERENCES course_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: session_id_refs_id_30c35cb5cd7cfb70; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_enrollment
    ADD CONSTRAINT session_id_refs_id_30c35cb5cd7cfb70 FOREIGN KEY (session_id) REFERENCES course_session(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: session_id_refs_id_6acf1c80b731c46a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_classtime
    ADD CONSTRAINT session_id_refs_id_6acf1c80b731c46a FOREIGN KEY (session_id) REFERENCES course_session(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: site_id_refs_id_44940f11a9977a78; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_sites
    ADD CONSTRAINT site_id_refs_id_44940f11a9977a78 FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: status_id_refs_id_35ec5af709b761db; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article
    ADD CONSTRAINT status_id_refs_id_35ec5af709b761db FOREIGN KEY (status_id) REFERENCES articles_articlestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subject_id_refs_id_4d8898786517417a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_course_subjects
    ADD CONSTRAINT subject_id_refs_id_4d8898786517417a FOREIGN KEY (subject_id) REFERENCES course_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tag_id_refs_id_44e3b8e865127384; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_tags
    ADD CONSTRAINT tag_id_refs_id_44e3b8e865127384 FOREIGN KEY (tag_id) REFERENCES articles_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: template_id_refs_id_6b55fc5ab6ea49bc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY content_sidebarwidget
    ADD CONSTRAINT template_id_refs_id_6b55fc5ab6ea49bc FOREIGN KEY (template_id) REFERENCES content_template(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: term_id_refs_id_5931f3ba57bbbc3d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section
    ADD CONSTRAINT term_id_refs_id_5931f3ba57bbbc3d FOREIGN KEY (term_id) REFERENCES course_term(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: to_article_id_refs_id_1bf7090e87599599; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_followup_for
    ADD CONSTRAINT to_article_id_refs_id_1bf7090e87599599 FOREIGN KEY (to_article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: to_article_id_refs_id_4fe177d23bb1e638; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles_article_related_articles
    ADD CONSTRAINT to_article_id_refs_id_4fe177d23bb1e638 FOREIGN KEY (to_article_id) REFERENCES articles_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tool_id_refs_id_19f35627560a7a9a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolphoto
    ADD CONSTRAINT tool_id_refs_id_19f35627560a7a9a FOREIGN KEY (tool_id) REFERENCES tool_tool(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tool_id_refs_id_2a6bcdb24f7a431f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toollink
    ADD CONSTRAINT tool_id_refs_id_2a6bcdb24f7a431f FOREIGN KEY (tool_id) REFERENCES tool_tool(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tool_id_refs_id_33d5af3444b2e675; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tool_toolvideo
    ADD CONSTRAINT tool_id_refs_id_33d5af3444b2e675 FOREIGN KEY (tool_id) REFERENCES tool_tool(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tool_id_refs_id_47fd41ffc4c34e2a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_section_tools
    ADD CONSTRAINT tool_id_refs_id_47fd41ffc4c34e2a FOREIGN KEY (tool_id) REFERENCES tool_tool(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_3512e549d157d780; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_profile
    ADD CONSTRAINT user_id_refs_id_3512e549d157d780 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_4a3341d94b86cfe3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_enrollment
    ADD CONSTRAINT user_id_refs_id_4a3341d94b86cfe3 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_4dd3626e643d7c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY membership_survey
    ADD CONSTRAINT user_id_refs_id_4dd3626e643d7c FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_70342d17d433860; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY course_session
    ADD CONSTRAINT user_id_refs_id_70342d17d433860 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_831107f1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_831107f1 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_f2045483; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_f2045483 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

