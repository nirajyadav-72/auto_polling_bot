# =====================================================================
# 🗑️ BOT CLEANUP HANDLER - DATABASE से GROUP DELETE करना
# =====================================================================

import sqlite3
import time

def cleanup_group_data(chat_id, DB_FILE):
    """
    जब bot किसी group से remove हो, तो उस group का सभी data delete करो
    """
    try:
        with sqlite3.connect(DB_FILE, timeout=20) as conn:
            cursor = conn.cursor()
            
            # 1. groups table से delete करो
            cursor.execute("DELETE FROM groups WHERE chat_id = ?", (chat_id,))
            deleted_groups = cursor.rowcount
            
            # 2. poll_mapping से delete करो
            cursor.execute("DELETE FROM poll_mapping WHERE chat_id = ?", (chat_id,))
            deleted_polls = cursor.rowcount
            
            # 3. daily_scores से delete करो
            cursor.execute("DELETE FROM daily_scores WHERE chat_id = ?", (chat_id,))
            deleted_scores = cursor.rowcount
            
            conn.commit()
        
        print(f"🗑️ [GROUP {chat_id}] Cleanup Complete!")
        print(f"   ✅ Groups: {deleted_groups} | Polls: {deleted_polls} | Scores: {deleted_scores}")
        
    except Exception as e:
        print(f"❌ [GROUP {chat_id}] Cleanup failed: {e}")


def get_group_storage_size(chat_id, DB_FILE):
    """
    किसी group की storage size check करो
    """
    try:
        with sqlite3.connect(DB_FILE, timeout=20) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM groups WHERE chat_id = ?", (chat_id,))
            groups_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM poll_mapping WHERE chat_id = ?", (chat_id,))
            polls_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM daily_scores WHERE chat_id = ?", (chat_id,))
            scores_count = cursor.fetchone()[0]
            
            total = groups_count + polls_count + scores_count
            return {
                "chat_id": chat_id,
                "groups": groups_count,
                "polls": polls_count,
                "scores": scores_count,
                "total": total
            }
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def database_stats(DB_FILE):
    """
    Database की पूरी statistics
    """
    try:
        with sqlite3.connect(DB_FILE, timeout=20) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM groups")
            total_groups = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM poll_mapping")
            total_polls = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM daily_scores")
            total_scores = cursor.fetchone()[0]
            
            return {
                "groups": total_groups,
                "users": total_users,
                "polls": total_polls,
                "scores": total_scores,
                "total": total_groups + total_users + total_polls + total_scores
            }
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
