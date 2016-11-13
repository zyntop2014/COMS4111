COPY administrator (admin_id, email, user_name, encrypted_password) FROM stdin;
1	volutpat@enimSuspendissealiquet.co.uk	Gregory Sandoval	4008
2	mollis.Phasellus.libero@sedduiFusce.co.uk	Denton P. Holloway	9491
3	Etiam@nuncQuisqueornare.edu	Garth P. Burch	2891
4	urna.Nunc@ettristiquepellentesque.com	Uta U. Velez	5160
5	aliquam.adipiscing.lacus@eu.co.uk	Delilah F. Allen	6680
6	molestie.orci@Suspendisse.ca	Glenna L. Hall	6789
7	dictum@velitjusto.co.uk	Colette P. Ballard	3809
8	fringilla@acmetusvitae.net	Velma W. Hensley	9283
9	egestas.lacinia@Aliquamauctor.org	Lila R. Nicholson	9754
10	Curabitur.sed.tortor@ullamcorperDuis.ca	Juliet J. Brown	5258
\.


--
-- TOC entry 3228 (class 0 OID 22300)
-- Dependencies: 567
-- Data for Name: customer; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY customer (customer_id, first_name, last_name, phone_number, customer_email) FROM stdin;
1	Garrison	Mckay	(846) 503-1084	parturient.montes@ridiculusmusProin.com
2	Salvador	Monroe	(194) 968-6497	gravida.Aliquam@utsemNulla.co.uk
3	Cameron	Newman	(122) 472-7949	turpis.vitae@Donecnibhenim.net
4	Prescott	Little	(746) 164-1043	convallis.dolor@egetvarius.edu
5	Matthew	Snyder	(663) 440-2762	massa.lobortis@vitaealiquet.com
6	Petra	Gentry	(602) 402-7528	placerat@Sedidrisus.org
7	Melyssa	Hardy	(192) 476-4316	nunc@justositamet.edu
8	Whoopi	Morgan	(718) 966-1254	in@lectus.com
9	Octavius	Savage	(121) 963-5505	eget@dapibus.co.uk
10	Raya	Mckenzie	(448) 584-6159	lorem.ut.aliquam@ornarelectus.net
\.


--
-- TOC entry 3233 (class 0 OID 22332)
-- Dependencies: 572
-- Data for Name: manage; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY manage (restaurant_id, admin_id) FROM stdin;
2	8
7	5
4	2
10	6
5	3
4	7
5	5
4	1
3	6
2	1
3	8
9	8
1	3
6	9
8	10
2	4
\.


--
-- TOC entry 3230 (class 0 OID 22313)
-- Dependencies: 569
-- Data for Name: notification; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY notification (body, type, sent_at, restaurant_id, customer_id) FROM stdin;
Your table is ready	TABLE_READY	2016-10-05 12:57:38	10	4
Your table is ready	TABLE_READY	2016-10-06 12:38:23	9	6
Your table is ready	TABLE_READY	2016-10-02 14:29:05	8	9
Your table is ready	TABLE_READY	2016-10-08 23:35:58	9	4
Your table is ready	TABLE_READY	2016-10-11 08:06:34	3	10
Your table is ready	TABLE_READY	2016-10-12 15:30:04	4	10
Your table is ready	TABLE_READY	2016-10-07 04:08:42	3	1
Your table is ready	TABLE_READY	2016-10-06 21:46:13	10	5
Your table is ready	TABLE_READY	2016-10-03 20:53:46	2	5
Your table is ready	TABLE_READY	2016-10-06 19:06:56	8	6
Your table is ready	TABLE_READY	2016-10-06 04:13:07	6	1
Your table is ready	TABLE_READY	2016-10-04 01:09:02	5	1
Your table is ready	TABLE_READY	2016-10-01 13:07:34	8	7
Your table is ready	TABLE_READY	2016-10-05 17:37:26	2	5
Your table is ready	TABLE_READY	2016-10-08 20:08:50	1	5
Your table is ready	TABLE_READY	2016-10-04 16:33:40	9	6
Your table is ready	TABLE_READY	2016-10-07 20:09:59	6	1
Your table is ready	TABLE_READY	2016-10-09 19:49:56	2	10
Your table is ready	TABLE_READY	2016-10-09 17:44:59	7	1
Your table is ready	TABLE_READY	2016-10-01 13:11:22	10	5
Your table is ready	TABLE_READY	2016-10-02 19:55:22	3	8
Your table is ready	TABLE_READY	2016-10-04 12:16:08	4	4
Your table is ready	TABLE_READY	2016-10-05 11:54:36	8	4
Your table is ready	TABLE_READY	2016-10-06 13:00:27	8	6
\.


--
-- TOC entry 3229 (class 0 OID 22307)
-- Dependencies: 568
-- Data for Name: party; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY party (size, customer_id, party_datetime, table_id, restaurant_id, seated_datetime, finish_at) FROM stdin;
3	4	2016-10-05 11:38:23	\N	\N	\N	\N
7	5	2016-10-03 20:49:07	4	2	2016-10-03 21:39:49	2016-10-03 23:29:38
4	6	2016-10-06 18:32:25	3	8	2016-10-06 19:07:44	2016-10-06 20:31:28
4	5	2016-10-09 19:28:17	4	6	2016-10-09 19:37:13	2016-10-09 22:19:26
2	6	2016-10-06 12:00:39	\N	\N	\N	\N
1	2	2016-10-01 18:03:39	1	6	2016-10-01 18:33:39	2016-10-01 20:03:39
5	9	2016-10-02 13:46:13	\N	\N	\N	\N
5	4	2016-10-08 22:34:03	\N	\N	\N	\N
2	10	2016-10-11 07:34:29	\N	\N	\N	\N
4	10	2016-10-12 15:23:40	\N	\N	\N	\N
1	5	2016-10-05 17:13:57	4	2	2016-10-05 17:53:57	2016-10-05 19:45:57
3	5	2016-10-08 20:00:00	3	1	2016-10-08 20:17:56	2016-10-08 21:19:42
1	6	2016-10-04 16:25:36	1	9	2016-10-04 17:00:00	2016-10-04 18:17:36
6	1	2016-10-10 18:12:54	4	4	2016-10-10 19:00:04	2016-10-10 21:12:04
1	1	2016-10-07 20:09:10	3	6	2016-10-07 20:09:10	2016-10-07 21:39:10
6	10	2016-10-09 19:35:35	1	2	2016-10-09 20:11:55	2016-10-09 21:12:34
3	6	2016-10-02 20:30:20	2	1	2016-10-02 21:26:10	2016-10-02 23:33:14
5	8	2016-10-09 13:25:28	1	2	2016-10-09 14:10:53	2016-10-09 14:33:34
3	1	2016-10-09 17:08:02	2	7	2016-10-09 17:50:31	2016-10-09 19:02:26
1	5	2016-10-01 12:44:43	4	10	2016-10-01 13:35:48	2016-10-01 15:00:57
6	8	2016-10-02 19:54:58	3	3	2016-10-02 19:54:58	2016-10-02 20:34:58
2	4	2016-10-04 12:14:48	3	4	2016-10-04 12:14:48	2016-10-04 13:14:48
2	3	2016-10-10 21:00:00	1	6	2016-10-10 21:15:49	2016-10-10 23:40:49
7	1	2016-10-04 15:14:23	1	5	2016-10-02 15:55:38	2016-10-09 17:06:55
6	6	2016-10-01 22:44:13	5	1	2016-10-01 19:26:50	2016-10-01 21:36:37
2	1	2016-10-02 11:49:06	2	3	2016-10-02 12:34:27	2016-10-02 14:04:44
3	5	2016-10-06 21:44:52	2	10	2016-10-06 21:44:52	2016-10-07 00:41:50
4	1	2016-10-05 23:43:54	2	6	2016-10-05 23:47:31	2016-10-06 00:39:01
2	7	2016-10-01 08:41:54	1	8	2016-10-01 09:04:09	2016-10-01 10:06:20
\.


--
-- TOC entry 3227 (class 0 OID 22295)
-- Dependencies: 566
-- Data for Name: restaurant; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY restaurant (restaurant_id, name) FROM stdin;
1	Le Bernardin
2	Bouley
3	Daniel
4	Jean-Georges
5	Gotham Bar and Grill
6	Peter Luger Steak House
7	Eleven Madison Park
8	Blue Hill
9	Per Se
10	Gramercy Tavern
\.


--
-- TOC entry 3231 (class 0 OID 22321)
-- Dependencies: 570
-- Data for Name: restaurant_table; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY restaurant_table (table_id, seats, restaurant_id) FROM stdin;
1	2	1
2	8	1
3	4	1
4	6	1
5	6	1
1	8	2
2	8	2
3	4	2
4	7	2
5	5	2
1	4	3
2	2	3
3	6	3
1	2	4
2	7	4
3	2	4
4	6	4
1	7	5
2	3	5
3	3	5
4	6	5
1	2	6
2	4	6
3	5	6
4	4	6
5	6	6
1	2	7
2	6	7
3	7	7
1	2	8
2	5	8
3	4	8
4	7	8
1	4	9
2	4	9
3	4	9
4	5	9
5	5	9
1	8	10
2	5	10
3	4	10
4	3	10
\.


--
-- TOC entry 3232 (class 0 OID 22327)
-- Dependencies: 571
-- Data for Name: waitlist; Type: TABLE DATA; Schema: postgres; Owner: postgres
--

COPY waitlist (restaurant_id, customer_id, party_datetime, listed_at, unlisted_at) FROM stdin;
8	4	2016-10-05 11:38:23	2016-10-05 12:18:23	2016-10-05 12:58:23
2	6	2016-10-06 12:00:39	2016-10-06 12:05:39	2016-10-06 15:10:39
6	2	2016-10-01 18:03:39	2016-10-01 18:08:39	2016-10-01 18:33:39
10	9	2016-10-02 13:46:13	2016-10-02 13:47:13	2016-10-02 16:47:13
2	4	2016-10-08 22:34:03	2016-10-08 22:38:03	2016-10-09 00:18:03
9	10	2016-10-11 07:34:29	2016-10-11 07:35:29	2016-10-11 09:55:29
2	10	2016-10-12 15:23:40	2016-10-12 15:25:40	2016-10-12 16:34:40
2	5	2016-10-05 17:13:57	2016-10-05 17:13:57	2016-10-05 17:53:57
1	5	2016-10-08 20:00:00	2016-10-08 20:01:00	2016-10-08 20:17:56
9	6	2016-10-04 16:25:36	2016-10-04 16:29:36	2016-10-04 17:00:00
4	1	2016-10-10 18:12:54	2016-10-10 18:14:54	2016-10-10 19:00:04
2	10	2016-10-09 19:35:35	2016-10-09 19:40:35	2016-10-09 20:11:55
1	6	2016-10-02 20:30:20	2016-10-02 20:34:20	2016-10-02 21:26:10
2	8	2016-10-09 13:25:28	2016-10-09 13:29:28	2016-10-09 14:10:53
7	1	2016-10-09 17:08:02	2016-10-09 17:12:02	2016-10-09 17:50:31
10	5	2016-10-01 12:44:43	2016-10-01 12:47:43	2016-10-01 13:35:48
6	3	2016-10-10 21:00:00	2016-10-10 21:01:00	2016-10-10 21:15:49
3	1	2016-10-02 11:49:06	2016-10-02 11:49:06	2016-10-02 12:34:27
6	1	2016-10-05 23:43:54	2016-10-05 23:44:00	2016-10-05 23:47:31
8	7	2016-10-01 08:41:54	2016-10-01 08:42:54	2016-10-01 09:04:09
\.:set 
