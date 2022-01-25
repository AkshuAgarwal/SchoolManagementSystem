import { createContext, useState } from 'react';

const SidebarContext = createContext({
    selected    : null,
    setSelected : () => {},
    open        : false,
    setOpen     : () => {},
});

export default SidebarContext;

export const SidebarProvider = ({ children }) => {
    const [ sidebarOpen, setSidebarOpen ] = useState(false);
    const [ selectedItem, setSelectedItem ] = useState(null);

    const contextData = {
        selected    : selectedItem,
        setSelected : setSelectedItem,
        open        : sidebarOpen,
        setOpen     : setSidebarOpen,
    };

    return (
        <SidebarContext.Provider value={contextData}>
            {children}
        </SidebarContext.Provider>
    );
};
