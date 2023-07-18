import Header from 'components/Header';
import { Outlet } from 'react-router-dom';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import './styles.scss'

export default function App() {
    return (
        <>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <div className="app">
                    <Header />
                    <div className="app-body">
                        <Outlet />
                    </div>
                </div>
            </LocalizationProvider>
        </>
    );
}
