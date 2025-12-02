"""
Migration script to add user_id column to analysis_results table
"""
from database.connection import engine
from sqlalchemy import text

def migrate():
    print("Starting migration...")

    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='analysis_results' AND column_name='user_id'
        """))

        if result.fetchone():
            print("✓ user_id column already exists. No migration needed.")
            return

        # Add user_id column (nullable first, since existing rows need it)
        print("Adding user_id column...")
        conn.execute(text("""
            ALTER TABLE analysis_results
            ADD COLUMN user_id INTEGER
        """))
        conn.commit()

        # Set default user_id for existing rows (use first user)
        print("Setting default user_id for existing records...")
        conn.execute(text("""
            UPDATE analysis_results
            SET user_id = (SELECT id FROM users LIMIT 1)
            WHERE user_id IS NULL
        """))
        conn.commit()

        # Make user_id NOT NULL
        print("Making user_id NOT NULL...")
        conn.execute(text("""
            ALTER TABLE analysis_results
            ALTER COLUMN user_id SET NOT NULL
        """))
        conn.commit()

        # Add foreign key constraint
        print("Adding foreign key constraint...")
        conn.execute(text("""
            ALTER TABLE analysis_results
            ADD CONSTRAINT fk_user_id
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        """))
        conn.commit()

        # Add index
        print("Adding index on user_id...")
        conn.execute(text("""
            CREATE INDEX ix_analysis_results_user_id ON analysis_results(user_id)
        """))
        conn.commit()

        print("✓ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
