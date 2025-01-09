import React, { useEffect, useState } from 'react';
import { database } from "./firebase";
import { ref, get } from "firebase/database";
import './DataTable.css';

const StudentClubs = () => {
    const [data, setData] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchClubs = async () => {
            try {
                const clubsRef = ref(database, "clubhub");
                const snapshot = await get(clubsRef);

                if (snapshot.exists()) {
                    setData(Object.values(snapshot.val()));
                } else {
                    console.log("No data available");
                }

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchClubs();
    }, []);

    const filteredData = data.filter(item =>
        item.Club?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.Description?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) return <div>Loading...</div>;

    return (
        <div className="data-table-container">
            <input
                type="text"
                placeholder="Search clubs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
            />
            <table className="data-table">
                <thead>
                    <tr>
                        <th>Club</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredData.map((item, index) => (
                        <tr key={index}>
                            <td>{item.Club}</td>
                            <td>{item.Description}</td>
                            <td>{item.Category}</td>
                            <td>
                                {item.Link && (
                                    <a href={item.Link}
                                        target="_blank"
                                        rel="noopener noreferrer">
                                        Visit
                                    </a>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default StudentClubs;