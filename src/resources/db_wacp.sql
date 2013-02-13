-- ----------------------------
--  Sequence structure for "apc_config_id_seq"
-- ----------------------------
--DROP SEQUENCE IF EXISTS "apc_config_id_seq";
CREATE SEQUENCE "apc_config_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "apc_config_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "apc_device_id_seq"
-- ----------------------------
--DROP SEQUENCE IF EXISTS "apc_device_id_seq";
CREATE SEQUENCE "apc_device_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "apc_device_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "apc_device"
-- ----------------------------
--DROP TABLE IF EXISTS "apc_device";
CREATE TABLE "apc_device" (
	"id" int4 NOT NULL DEFAULT nextval('apc_device_id_seq'::regclass),
	"nick" char(255),
	"ip" inet,
	"config_id" int2,
	"username" char(255),
	"password" char(255),
	"date_added" timestamp(6) NULL,
	"date_modified" timestamp(6) NULL
);
--WITH (OIDS=FALSE);
ALTER TABLE "apc_device" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "apc_config"
-- ----------------------------
--DROP TABLE IF EXISTS "apc_config";
CREATE TABLE "apc_config" (
	"id" int4 NOT NULL DEFAULT nextval('apc_config_id_seq'::regclass),
	"name" char(255),
	"description" char(255),
	"ip" inet,
	"radius_config_id" int2,
	"ssid" char(255),
	"vlan_id" int2,
	"channel" int2,
	"channel_freq" char(255),
	"date_added" timestamp(6) NULL,
	"date_modified" timestamp(6) NULL
);
--WITH (OIDS=FALSE);
ALTER TABLE "apc_config" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "apc_groups"
-- ----------------------------
--DROP TABLE IF EXISTS "apc_groups";
CREATE TABLE "apc_groups" (
	"id" int2 NOT NULL DEFAULT nextval('apc_groups_id_seq'::regclass),
	"name" char(255) NOT NULL,
	"config_id" smallint
);
--WITH (OIDS=FALSE);
ALTER TABLE "apc_groups" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "apc_device_group"
-- ----------------------------
--DROP TABLE IF EXISTS "apc_device_group";
CREATE TABLE "apc_device_group" (
	"group_id" int2 NOT NULL,
	"device_id" int2 NOT NULL
);
--WITH (OIDS=FALSE);
ALTER TABLE "apc_device_group" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "apc_vlan"
-- ----------------------------
--DROP TABLE IF EXISTS "apc_vlan";
CREATE TABLE "apc_vlan" (
	"id" int2 NOT NULL DEFAULT nextval('apc_vlan_id_seq'::regclass),
	"name" char(255),
	"ip" inet,
	"subnet" inet,
	"number" char(255),
	"interface" char(255)
);
--WITH (OIDS=FALSE);
ALTER TABLE "apc_vlan" OWNER TO "postgres";


-- ----------------------------
--  Alter sequences owned by
-- ----------------------------
--ALTER SEQUENCE "apc_config_id_seq" OWNED BY "apc_config"."id";
--ALTER SEQUENCE "apc_device_id_seq" OWNED BY "apc_device"."id";
-- ----------------------------
--  Primary key structure for table "apc_device"
-- ----------------------------
ALTER TABLE "apc_device" ADD CONSTRAINT "apc_device_pkey" PRIMARY KEY ("id") ;

-- ----------------------------
--  Primary key structure for table "apc_config"
-- ----------------------------
ALTER TABLE "apc_config" ADD CONSTRAINT "apc_config_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "apc_groups"
-- ----------------------------
ALTER TABLE "apc_groups" ADD CONSTRAINT "apc_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "apc_vlan"
-- ----------------------------
ALTER TABLE "apc_vlan" ADD CONSTRAINT "apc_vlan_pkey" PRIMARY KEY ("id");

