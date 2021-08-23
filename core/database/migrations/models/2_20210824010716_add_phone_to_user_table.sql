-- upgrade --
ALTER TABLE "user" ADD "phone" VARCHAR(25);
-- downgrade --
ALTER TABLE "user" DROP COLUMN "phone";
