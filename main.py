from cpu_scheduling import cpu_menu
from memory_allocation import memory_menu
from page_replacement import page_menu


def main():
    while True:
        print("\n" + "=" * 60)
        print("OPERATING SYSTEMS PROJECT")
        print("=" * 60)
        print("1) CPU Scheduling")
        print("2) Memory Allocation")
        print("3) Page Replacement")
        print("4) Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            cpu_menu()
        elif choice == "2":
            memory_menu()
        elif choice == "3":
            page_menu()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()