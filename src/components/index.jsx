import React, { useEffect, useState } from "react";
import axios from "axios";
import { BiChevronUp, BiChevronDown } from 'react-icons/bi';

export default function Search() {
  const [query, setQuery] = useState("");
  const [jobtitle, setJobTitle] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [provinceData, setProvinceData] = useState([]);
  const [selected, setSelected] = useState("");
  const [open, setOpen] = useState(false);
  const [islinkedinchecked, setIsLinkedinChecked] = useState(true);
  const [isindeedchecked, setIsIndeedChecked] = useState(false);
  const [linkedinquery, setLinkedInQuery] = useState([]);

  const provinces = ["Calgary", "Toronto", "Vancouver", "Montreal", "Quebec"];
  
  useEffect(() => {
    setProvinceData(provinces);
  }, []);

  const options = {
    method: "GET",
    url: "https://google-search74.p.rapidapi.com/",
    params: {
      query: "Nike",
      limit: "10",
      related_keywords: "true",
    },
    headers: {
      "x-rapidapi-key": import.meta.env.VITE_REACT_APP_RAPIDAPI_KEY,
      "x-rapidapi-host": "google-search74.p.rapidapi.com",
    },
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.request(options);
      setResults(response.data.results);
      console.log(results);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  // const handleLinkedinJobsSearch = async = () => {
  //     setLoading(true);
  //     try {
  //         const linkedinjobs = await axios.request({

  //         })
  //     }
  //     setLoading(false);
  // }

  return (
    <div className="p-4">
      <div className="flex-col mb-4">
        <h3>Select the job search websites (to get job postings)</h3>
        <input type="checkbox" checked={islinkedinchecked} onChange={() => setIsLinkedinChecked(!islinkedinchecked)} id="select-linkedin" className="p-2 mr-1" />
        <label htmlFor="select-linkedin" className="text-black">
          LinkedIn
        </label>
        <input type="checkbox" checked={isindeedchecked} onChange={() => setIsIndeedChecked(!isindeedchecked)} id="select-indeed" className="p-2 ml-4 mr-1" />
        <label htmlFor="select-indeed" className="text-black">
          Indeed
        </label>
      </div>
      <div className="flex justify-center items-center">
        <h3 className="mr-2 font-semibold">Job title:</h3>
        <input
          type="text"
          value={jobtitle}
          placeholder="job title"
          onChange={(e) => setJobTitle(e.target.value)}
          className="border border-gray-300 p-2 rounded bg-gray-300"
        />
      </div>
      {/* <button id="dropdownDefaultButton" data-dropdown-toggle="dropdown" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">Dropdown button <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6"> */}

      <div>
        <h3 className="mt-6 items-center inline-flex font-semibold">
          Select city(Canada):
          <div className=" border border-gray-300 p-1 rounded hover:bg-gray-200 flex items-center justify-between px-2 ml-2" onClick={() => setOpen(!open)}>
            {selected ? selected : "Calgary"}
            {open ? <BiChevronUp size={20} /> : <BiChevronDown size={20} />}
          </div>
        </h3>
        <ul
          className={`bg-white mt-2 ml-20 pl-20 overflow-y-auto ${open ? 'max-h-60':'max-h-0'}`}
        >
          {provinceData?.map((province) => (
            <li
              key={province}
              className="p-2 text-sm hover:bg-sky-600 hover:text-white"
              onClick={() => {
                if (province?.toLowerCase() !== selected.toLowerCase()) {
                  setSelected(province);
                  setOpen(false);
                }
              }}
            >
              {province}
            </li>
          ))}
        </ul>
      </div>
      {/* {/* <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..." className='border border-gray-300 p-2 rounded'/> */}
      <button
        onClick={handleSearch}
        className="ml-2 mt-6 p-2 bg-red-500 text-white rounded"
      >
        Search for Jobs
      </button>
      {loading && <p>Loading...</p>}
    </div>
  );
}
