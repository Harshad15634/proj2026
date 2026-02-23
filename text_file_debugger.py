import os
import sys
import stat
import platform
from pathlib import Path

def diagnose_file_operation(filepath, mode='a'):
    """
    Comprehensive diagnostic for file operation errors
    Returns: (success, message, fix_suggestions)
    """
    print("=" * 60)
    print(f"🔍 DIAGNOSING FILE OPERATION: '{filepath}' (mode: '{mode}')")
    print("=" * 60)
    
    issues = []
    fixes = []
    
    # Convert to Path object for easier manipulation
    path = Path(filepath)
    absolute_path = path.absolute()
    
    # System info
    print(f"\n📋 SYSTEM INFORMATION:")
    print(f"  • OS: {platform.system()} {platform.release()}")
    print(f"  • Python: {sys.version}")
    print(f"  • Working directory: {os.getcwd()}")
    print(f"  • Absolute path: {absolute_path}")
    
    # Check 1: Parent directory exists
    print(f"\n📁 CHECKING PARENT DIRECTORY:")
    parent_dir = path.parent
    
    if not parent_dir.exists():
        issues.append("PARENT_DIR_MISSING")
        print(f"  ❌ Parent directory does not exist: {parent_dir}")
        
        # Try to find if any part of the path exists
        current = absolute_path
        existing_path = None
        while current != current.parent:
            if current.exists():
                existing_path = current
                break
            current = current.parent
        
        if existing_path:
            print(f"  ℹ️  Last existing part: {existing_path}")
            missing_part = str(absolute_path).replace(str(existing_path), "").lstrip("/\\")
            fixes.append(f"Create the missing directories: os.makedirs('{parent_dir}')")
        else:
            fixes.append(f"Create the full directory structure: os.makedirs('{parent_dir}')")
    else:
        print(f"  ✅ Parent directory exists: {parent_dir}")
        
        # Check parent directory permissions
        parent_perms = oct(os.stat(parent_dir).st_mode)[-3:]
        print(f"  ℹ️  Parent directory permissions: {parent_perms}")
        
        if not os.access(parent_dir, os.W_OK):
            issues.append("PARENT_NOT_WRITABLE")
            print(f"  ❌ No write permission on parent directory")
            fixes.append(f"Change permissions: chmod +w '{parent_dir}' or run with appropriate privileges")
    
    # Check 2: Filename validity
    print(f"\n📝 CHECKING FILENAME VALIDITY:")
    invalid_chars = []
    
    if platform.system() == "Windows":
        # Windows invalid characters
        windows_invalid = '<>:"/\\|?*'
        for char in windows_invalid:
            if char in path.name:
                invalid_chars.append(char)
        
        # Windows reserved names
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                          'LPT1', 'LPT2', 'LPT3']
        name_without_ext = path.stem.upper()
        if name_without_ext in reserved_names:
            issues.append("RESERVED_FILENAME")
            print(f"  ❌ '{name_without_ext}' is a reserved Windows filename")
            fixes.append(f"Rename the file to something not in: {reserved_names}")
    else:
        # Unix-like systems - only / and null are invalid
        if '/' in path.name:
            invalid_chars.append('/')
        if '\0' in path.name:
            invalid_chars.append('\\0')
    
    if invalid_chars:
        issues.append("INVALID_CHARACTERS")
        print(f"  ❌ Invalid characters in filename: {invalid_chars}")
        fixes.append(f"Remove these characters from filename: {invalid_chars}")
    else:
        print(f"  ✅ Filename appears valid")
    
    # Check 3: File existence and permissions
    print(f"\n📄 CHECKING FILE:")
    if path.exists():
        print(f"  ✅ File exists")
        
        # Check if it's a file (not directory)
        if path.is_dir():
            issues.append("IS_DIRECTORY")
            print(f"  ❌ Path is a directory, not a file")
            fixes.append(f"Use a different name or remove the directory: rmdir '{path}'")
        
        # Check permissions
        if not os.access(path, os.W_OK):
            issues.append("FILE_NOT_WRITABLE")
            print(f"  ❌ No write permission on file")
            fixes.append(f"Change permissions: chmod +w '{path}'")
        else:
            print(f"  ✅ File is writable")
        
        # Check if file is locked (Windows specific)
        if platform.system() == "Windows":
            try:
                # Try to open exclusively to check if locked
                fd = os.open(path, os.O_RDWR | os.O_EXCL)
                os.close(fd)
                print(f"  ✅ File is not locked by another process")
            except OSError:
                issues.append("FILE_LOCKED")
                print(f"  ❌ File is locked by another process")
                fixes.append(f"Close the file in other programs or wait for the lock to release")
    else:
        print(f"  ℹ️  File does not exist yet (will be created)")
    
    # Check 4: Disk space
    print(f"\n💾 CHECKING DISK SPACE:")
    try:
        statvfs = os.statvfs(parent_dir if parent_dir.exists() else '/')
        free_space = statvfs.f_frsize * statvfs.f_bavail
        free_space_mb = free_space / (1024 * 1024)
        
        print(f"  ℹ️  Free disk space: {free_space_mb:.2f} MB")
        
        if free_space < 1024 * 1024:  # Less than 1MB
            issues.append("LOW_DISK_SPACE")
            print(f"  ⚠️  Very low disk space!")
            fixes.append(f"Free up disk space on this drive")
    except:
        print(f"  ℹ️  Could not check disk space")
    
    # Check 5: Try the actual operation with detailed error capture
    print(f"\n🔬 ATTEMPTING FILE OPERATION:")
    try:
        with open(path, mode) as f:
            f.write("Diagnostic test write\n")
        print(f"  ✅ SUCCESS! File operation completed without errors")
        
        # Clean up test write
        if path.exists() and path.stat().st_size == 0:
            path.unlink()
        
        return True, "File operation successful", ["No fixes needed"]
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"  ❌ ERROR: {error_type}: {error_msg}")
        
        # Map error to specific issue
        if "Permission denied" in error_msg:
            if "PARENT_NOT_WRITABLE" not in issues:
                issues.append("PERMISSION_DENIED")
                fixes.append("Run with appropriate permissions (maybe as administrator/sudo)")
        elif "No such file or directory" in error_msg and "PARENT_DIR_MISSING" not in issues:
            issues.append("PATH_NOT_FOUND")
            fixes.append(f"Create parent directory: os.makedirs('{parent_dir}', exist_ok=True)")
        elif "Invalid argument" in error_msg and "INVALID_CHARACTERS" not in issues:
            issues.append("INVALID_ARGUMENT")
            fixes.append("Check for hidden characters or extremely long path names")
        elif "Disk quota exceeded" in error_msg:
            issues.append("DISK_QUOTA")
            fixes.append("Free up disk space or increase quota")
        elif "Too many open files" in error_msg:
            issues.append("TOO_MANY_FILES")
            fixes.append("Close some file handles or increase system limit")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DIAGNOSIS SUMMARY:")
        print("=" * 60)
        
        if issues:
            print(f"\n❌ ISSUES FOUND ({len(issues)}):")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
            
            print(f"\n🔧 SUGGESTED FIXES:")
            for i, fix in enumerate(set(fixes), 1):  # Use set to remove duplicates
                print(f"  {i}. {fix}")
                
            print(f"\n💡 QUICK FIX ATTEMPT:")
            if "PARENT_DIR_MISSING" in issues:
                try:
                    os.makedirs(parent_dir, exist_ok=True)
                    print(f"  ✅ Created directory: {parent_dir}")
                    print(f"  ℹ️  Try running your file operation again")
                except Exception as dir_error:
                    print(f"  ❌ Could not create directory: {dir_error}")
        else:
            print(f"\n✅ No obvious issues found, but operation still failed.")
            print(f"⚠️  This might be a system-specific issue.")
            print(f"🔧 Try: Running with administrator/sudo privileges")
        
        return False, error_msg, fixes

def quick_fix_and_test(filepath, mode='a', content="Test content\n"):
    """
    Attempts to fix common issues and test the file operation
    """
    print("\n" + "🚀" * 30)
    print("🚀 ATTEMPTING AUTO-RECOVERY")
    print("🚀" * 30)
    
    path = Path(filepath)
    parent_dir = path.parent
    
    # Fix 1: Create parent directories if missing
    if not parent_dir.exists():
        try:
            os.makedirs(parent_dir, exist_ok=True)
            print(f"✅ Created missing directories: {parent_dir}")
        except Exception as e:
            print(f"❌ Could not create directories: {e}")
            return False
    
    # Fix 2: Check and fix permissions on Windows
    if platform.system() == "Windows" and path.exists():
        try:
            # On Windows, try to remove readonly attribute
            import stat
            os.chmod(path, stat.S_IWRITE)
            print(f"✅ Removed readonly attribute if present")
        except:
            pass
    
    # Try the operation again
    try:
        with open(path, mode) as f:
            f.write(content)
        print(f"✅ SUCCESS! File operation completed after fixes")
        print(f"📄 File written: {path}")
        return True
    except Exception as e:
        print(f"❌ Still failing: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    # Get filename from user or use default
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the filename you're trying to use: ").strip()
        if not filename:
            filename = "test.txt"
            print(f"Using default: {filename}")
    
    mode = input("Enter mode (default 'a' for append): ").strip() or 'a'
    
    # Run diagnosis
    success, message, fixes = diagnose_file_operation(filename, mode)
    
    if not success:
        print("\n" + "=" * 60)
        response = input("\n🔧 Would you like to attempt auto-fix? (y/n): ").lower()
        if response == 'y':
            quick_fix_and_test(filename, mode)
    
    print("\n" + "=" * 60)
    print("📌 TIPS FOR NEXT STEPS:")
    print("=" * 60)
    print("• Use absolute paths to avoid confusion: os.path.abspath('yourfile.txt')")
    print("• Always use 'with' statements for automatic cleanup")
    print("• Check disk space if files are large")
    print("• On Windows, avoid running from protected folders like 'Program Files'")
    print("• Consider using tempfile module for temporary files")