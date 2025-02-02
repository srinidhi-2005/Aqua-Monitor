import React, { useEffect, useRef, useCallback } from "react";

const Dropdown = ({ isOpen, toggleDropdown, navigateTo, darkMode, buttonRef }) => {
  const dropdownRef = useRef(null);

  const handleClickOutside = useCallback((event) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target) &&
      buttonRef.current &&
      !buttonRef.current.contains(event.target)
    ) {
      toggleDropdown();
    }
  }, [toggleDropdown, buttonRef]);

  const handleKeyDown = useCallback((event) => {
    if (event.key === "Escape") {
      toggleDropdown();
    }
  }, [toggleDropdown]);

  useEffect(() => {
    if (isOpen) {
      document.addEventListener("click", handleClickOutside);
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("click", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, handleClickOutside, handleKeyDown]);

  if (!isOpen) return null;

  return (
    <div
      ref={dropdownRef}
      role="menu"
      className={`absolute right-0 mt-2 w-48 rounded-md shadow-lg z-10 ${
        darkMode ? "bg-gray-800 text-gray-200" : "bg-white text-gray-800"
      }`}
    >
      <button
        onClick={() => {
          navigateTo("/profile");
          toggleDropdown();
        }}
        className="block px-4 py-2 hover:bg-blue-500 hover:text-white"
      >
        Profile
      </button>
      <button
        onClick={() => {
          navigateTo("/history");
          toggleDropdown();
        }}
        className="block px-4 py-2 hover:bg-blue-500 hover:text-white"
      >
        History
      </button>
    </div>
  );
};

export default Dropdown;